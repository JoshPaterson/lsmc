from operator import ge
from django.urls import path
from lsma import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('edit/title-page', views.EditTitlePageView.as_view()),
]