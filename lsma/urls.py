from operator import ge
from django.urls import path
from lsma import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('edit/title-page', views.EditTitlePageView.as_view()),
    path('edit/copyright-page', views.EditCopyrightPageView.as_view()),
    path('edit/title', views.EditTitleView.as_view()),
    path('edit/subtitle', views.EditSubtitleView.as_view()),
    path('edit/numbers-offset', views.EditNumbersOffsetView.as_view()),
    path('edit/roman-numbers-offset', views.EditRomanNumbersOffsetView.as_view()),
    path('edit/volume-number', views.EditVolumeNumberView.as_view()),
    path('edit/edition-number', views.EditEditionNumberView.as_view()),
    path('edit/issue-number', views.EditIssueNumberView.as_view()),
]