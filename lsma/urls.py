from operator import ge
from django.urls import path
from .views import generate_box_image

urlpatterns = [
    path('boxes/<str:book_slug>/<int:page>/<str:level>/<int:page_number>/<int:block_number>/<int:paragraph_number>/<int:line_number>/<int:word_number>', generate_box_image)
]