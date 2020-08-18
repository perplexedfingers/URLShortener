from django.urls import path

from . import views

urlpatterns = [
    path('redirect', views.redirect, name='redirect'),
    path('preview', views.preview, name='preview'),
    path('create', views.create, name='create'),
]
