from string import ascii_uppercase

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_uppercase_only(value):
    if any((char not in ascii_uppercase for char in value)):
        raise ValidationError(_('%(value)s is illegal'), params={'value': value}, code='invalid',)


class QueryForm(forms.Form):
    path_name = forms.CharField(label='Path name', max_length=5, min_length=5,
                                validators=[validate_uppercase_only])
    is_preview = forms.BooleanField(label='Select to preview. Deselect to redirect', required=False)


class CreateForm(forms.Form):
    url = forms.URLField(label='URL')
