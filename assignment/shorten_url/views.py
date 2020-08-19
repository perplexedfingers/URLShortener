from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET, require_POST

from .forms import CreateForm, QueryForm
from .models import Record, from_pk_to_char


@require_GET
def index(request):
    return render(request, 'index.html', {'query_form': QueryForm(), 'create_form': CreateForm()})


@require_GET
def convert(request):
    form = QueryForm(request.GET)
    form.is_valid()

    try:
        path_name = form.cleaned_data['path_name']
        url = Record.objects.get(path_name=path_name).url
    except Record.DoesNotExist:
        form.add_error('path_name', _(f'{path_name} coverts to nothing'))
    except KeyError:
        # When the path is illeagl, it is not in cleaned_data
        pass

    is_preview = form.cleaned_data['is_preview']

    if form.errors:
        return render(request, 'index.html', {'query_form': form.as_table(), 'create_form': CreateForm()})
    elif is_preview:
        return render(request, 'index.html', {'query_form': form.as_table(), 'create_form': CreateForm(),
                                              'url': url})
    else:
        return redirect(url)


@require_POST
def create(request):
    form = CreateForm(request.POST)
    if form.is_valid():
        url = form.cleaned_data['url']
        with transaction.atomic():
            record, is_created = Record.objects.get_or_create(url=url)
            if is_created:
                record.path_name = from_pk_to_char(record.pk)
                record.save()
        return render(request, 'index.html',
                      {'query_form': QueryForm({'path_name': record.path_name}).as_table(),
                       'create_form': CreateForm(),
                       'path_name': record.path_name})
    else:
        return render(request, 'index.html', {'query_form': QueryForm(), 'create_form': form.as_table()})
