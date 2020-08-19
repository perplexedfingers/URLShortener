from math import pow
from string import ascii_uppercase

from django.db import models

int_to_char = {int_: char for int_, char in enumerate(ascii_uppercase)}
ranks = tuple(pow(26, i) for i in range(5))


def from_pk_to_char(pk):
    result = ''
    for rank in reversed(ranks):
        result += int_to_char[pk // rank]
        pk %= rank
    return result


class Record(models.Model):
    url = models.URLField(unique=True)
    path_name = models.CharField(max_length=5, null=True)
