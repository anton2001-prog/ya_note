from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    ('notes:home', 'users:login', 'users:logout', 'users:signup')
)
def test_pages_availability_for_anonymous_user(not_author_client, name):
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK

# Добавляем к тесту ещё один декоратор parametrize; в его параметры
# нужно передать фикстуры-клиенты и ожидаемый код ответа для каждого клиента.


@pytest.mark.parametrize(
    # parametrized_client - название параметра,
    # в который будут передаваться фикстуры;
    # Параметр expected_status - ожидаемый статус ответа.
    'parametrized_client, expected_status',
    # В кортеже с кортежами передаём значения для параметров:
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete')
)
def test_pages_availability_for_different_users(
    parametrized_client, name, note_slug, expected_status
):
    url = reverse(name, args=note_slug)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    # Вторым параметром передаём note_object, 
    # в котором будет либо фикстура с объектом заметки, либо None.
    'name, args',
    (
        ('notes:detail', pytest.lazy_fixture('note_slug')),
        ('notes:edit', pytest.lazy_fixture('note_slug')),
        ('notes:delete', pytest.lazy_fixture('note_slug')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
#  Передаём в тест анонимный клиент, name проверяемых страниц и note_object
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
