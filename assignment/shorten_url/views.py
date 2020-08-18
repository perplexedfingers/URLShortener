from functools import wraps

from django.http import HttpResponse
from django.shortcuts import redirect as HTTP_redirect
from django.views.decorators.http import require_GET

from .models import Record, from_char_to_pk


def code_to_url(f):
    @wraps(f)
    def decorator(request, code, *args, **kws):
        pk = from_char_to_pk(code)
        url = Record.objects.get(pk=pk).URL
        return f(request, url, *args, **kws)
    return decorator


@require_GET
@code_to_url
def redirect(request, url):
    return HTTP_redirect(url)


@require_GET
@code_to_url
def preview(request, url):
    return HttpResponse(url)
