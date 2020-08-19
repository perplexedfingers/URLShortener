import pytest
from django.urls import reverse
from pytest_django.asserts import (assertContains, assertFormError,
                                   assertRedirects)

from .models import Record, from_char_to_pk, from_pk_to_char


def test_char_to_int():
    assert from_char_to_pk('AAAAB') == 1
    assert from_char_to_pk('AAABB') == 27
    assert from_char_to_pk('ZZZZZ') == 11881375

    with pytest.raises(ValueError):
        from_char_to_pk('ASDW')
    with pytest.raises(KeyError):
        from_char_to_pk('aaaab')
    with pytest.raises(TypeError):
        from_char_to_pk(123)


def test_int_to_char():
    assert from_pk_to_char(1) == 'AAAAB'
    assert from_pk_to_char(27) == 'AAABB'
    assert from_pk_to_char(10 ** 7 + 1) == 'VWYXL'

    with pytest.raises(KeyError):
        from_pk_to_char(10 ** 8)
    with pytest.raises(TypeError):
        from_pk_to_char('AAAAA')


def create_record(url):
    record = Record(url=url)
    record.save()
    record.path_name = from_pk_to_char(record.pk)
    record.save()
    return record


@pytest.mark.django_db
def test_redirect(client):
    test_url = 'http://test.io'
    record = create_record(test_url)
    response = client.get(reverse('convert'), {'path_name': record.path_name, 'is_preview': False})
    assertRedirects(response, test_url, fetch_redirect_response=False)


@pytest.mark.django_db
def test_preview(client):
    test_url = 'http://test.io'
    record = create_record(test_url)
    response = client.get(reverse('convert'), {'path_name': record.path_name, 'is_preview': True})
    assertContains(response, test_url)


@pytest.mark.django_db
def test_convert_to_nothing(client):
    test_path_name = 'A' * 5
    response = client.get(reverse('convert'), {'path_name': test_path_name, 'is_preview': True})
    assertFormError(response, 'query_form', 'path_name', f'{test_path_name} converts to nothing')


@pytest.mark.django_db
def test_illegal_path_name(client):
    test_path_name = 'a' * 5
    response = client.get(reverse('convert'), {'path_name': test_path_name, 'is_preview': True})
    assertFormError(response, 'query_form', 'path_name', f'{test_path_name} is illegal')


@pytest.mark.django_db
def test_create(client):
    test_url = 'http://test.io'
    response = client.post(reverse('create'), {'url': test_url})
    path_name = response.context['path_name']
    assert Record.objects.get(path_name=path_name)


@pytest.mark.django_db
def test_create_twice(client):
    test_url = 'http://test.io'
    response = client.post(reverse('create'), {'url': test_url})
    old_path_name = response.context['path_name']
    assert Record.objects.get(path_name=old_path_name)

    response = client.post(reverse('create'), {'url': test_url})
    new_path_name = response.context['path_name']
    assert new_path_name == old_path_name


@pytest.mark.django_db
def test_convert_illegal_URL(client):
    test_path_name = 'http://300.400.500.600'
    response = client.post(reverse('create'), {'url': test_path_name})
    assertFormError(response, 'create_form', 'url', 'Enter a valid URL.')


def test_trivial_test(client):
    response = client.get(reverse('index'))
    assert 'query_form' in response.context
    assert 'create_form' in response.context
