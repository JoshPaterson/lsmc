from operator import ge
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('edit/<slug:slug>', views.edit),
]