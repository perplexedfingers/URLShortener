from django.shortcuts import redirect as HTTP_redirect

from .models import Record, from_char_to_pk


def redirect(request, code):
    pk = from_char_to_pk(code)
    url = Record.objects.get(pk=pk).URL
    return HTTP_redirect(url)
