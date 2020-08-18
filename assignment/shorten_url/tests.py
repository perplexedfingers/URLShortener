import pytest

from .models import from_char_to_pk, from_pk_to_char


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
