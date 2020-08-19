from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST

from .forms import CreateForm, QueryForm
from .models import Record, from_pk_to_char


@require_GET
def convert(request):
    form = QueryForm(request.GET)
    if form.is_valid():
        path_name = form.cleaned_data['path_name']
        url = Record.objects.get(path_name=path_name).url
        is_redirect = form.cleaned_data['redirect_or_preview']
        if is_redirect:
            return redirect(url)
        else:
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
