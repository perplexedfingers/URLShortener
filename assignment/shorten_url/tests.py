import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects

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
    response = client.get(reverse('redirect'), {'path_name': record.path_name})
    assertRedirects(response, test_url, fetch_redirect_response=False)


@pytest.mark.django_db
def test_preview(client):
    test_url = 'http://test.io'
    record = create_record(test_url)
    response = client.get(reverse('preview'), {'path_name': record.path_name})
    assertContains(response, test_url)


@pytest.mark.django_db
def test_create(client):
    test_url = 'http://test.io'
    response = client.post(reverse('create'), {'url': test_url})
    path_name = response.content.decode('utf-8')
    assert Record.objects.get(path_name=path_name)
