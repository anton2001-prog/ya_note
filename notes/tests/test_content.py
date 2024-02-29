from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from pytils.translit import slugify
from notes.models import Note
from notes import forms

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author = User.objects.create(username='Anton')
        cls.notes = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )

    def test_note_ceate(self):
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_slug_create(self):
        field_slug = self.notes.slug
        title_slug = slugify(self.notes.title)
        self.assertEqual(field_slug, title_slug)
