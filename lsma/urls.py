from operator import ge
from django.urls import path
from lsma import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('edit/title-page', views.EditTitlePageView.as_view()),
    path('edit/copyright-page', views.EditCopyrightPageView.as_view()),
    path('edit/title', views.EditTitleView.as_view()),
    path('edit/subtitle', views.EditSubtitleView.as_view()),
]