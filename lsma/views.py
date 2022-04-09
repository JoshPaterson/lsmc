from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Page, Box
from PIL import Image
from io import BytesIO

def generate_box_image(request, book_slug, page, level, page_number, block_number, paragraph_number, line_number, word_number):
    book = Book.objects.get(slug=book_slug)
    page = book.pages.get(number=page)
    box = page.boxes.get(
        level=level,
        page_number=page_number,
        block_number=block_number,
        paragraph_number=paragraph_number,
        line_number=line_number,
        word_number=word_number)
    img = Image.open(box.original_image)
    # crop here
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    return HttpResponse(img_byte_arr.getvalue(), content_type="image/png")