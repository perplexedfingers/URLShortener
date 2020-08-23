from django.urls import path

from . import views

urlpatterns = [
    path('convert', views.convert, name='convert'),
    path('create', views.create, name='create'),
    path('', views.index, name='index'),
]
