from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Anton')
        cls.reader = User.objects.create(username='Reader')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug='zagolovok',
            author=cls.author
        )

    def test_homepage_availability(self):
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonimous_user(self):
        urls_to_redirect = (
            ('notes:add', None),
            ('notes:edit', (self.notes.slug,)),
            ('notes:detail', (self.notes.slug,)),
            ('notes:delete', (self.notes.slug,)),
            ('notes:list', None),
            ('notes:success', None)
        )
        login_url = reverse('users:login')

        for name, args in urls_to_redirect:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_availability_for_detail_edit_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND)
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:detail', 'notes:delete'):
                with self.subTest(name=name, user=user):
                    url = reverse(name, args=(self.notes.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)
