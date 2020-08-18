from functools import wraps

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect as HTTP_redirect
from django.views.decorators.http import require_GET, require_POST

from .forms import CreateForm, QueryForm
from .models import Record, from_pk_to_char


def path_name_to_url(f):
    @wraps(f)
    def decorator(request, *args, **kws):
        form = QueryForm(request.GET)
        if form.is_valid():
            path_name = form.cleaned_data['path_name']
            url = Record.objects.get(path_name=path_name).url
            return f(request, url, *args, **kws)
    return decorator


@require_GET
@path_name_to_url
def redirect(request, url):
    return HTTP_redirect(url)


@require_GET
@path_name_to_url
def preview(request, url):
    return HttpResponse(url)


@require_POST
def create(request):
    form = CreateForm(request.POST)
    if form.is_valid():
        url = form.cleaned_data['url']
        with transaction.atomic():
            record = Record(url=url)
            record.save()
            record.path_name = from_pk_to_char(record.pk)
            record.save()
        return HttpResponse(record.path_name)
