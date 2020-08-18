from math import pow
from string import ascii_uppercase

from django.db import models

char_to_int = {char: int_ for int_, char in enumerate(ascii_uppercase)}
int_to_char = {int_: char for int_, char in enumerate(ascii_uppercase)}
ranks = tuple(pow(26, i) for i in range(5))


def from_char_to_pk(chars):
    if len(chars) != 5:
        raise ValueError
    result = [char_to_int[char] * ranks[rank]
              for rank, char in enumerate(chars[::-1])]
    return int(sum(result))


def from_pk_to_char(pk):
    result = ''
    for rank in reversed(ranks):
        result += int_to_char[pk // rank]
        pk %= rank
    return result


class Record(models.Model):
    URL = models.URLField(unique=True)

    def to_chars(self):
        return from_pk_to_char(self.pk)
