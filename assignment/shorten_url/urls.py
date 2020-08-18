from django.urls import path

from . import views

urlpatterns = [
    path('<str:code>', views.redirect, name='redirect'),
    path('<str:code>/preview', views.preview, name='preview'),
]
