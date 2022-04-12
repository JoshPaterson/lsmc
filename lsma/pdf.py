from pikepdf import Pdf, PdfImage
from pikepdf.models.metadata import PdfMetadata
from lxml import etree
from uuid import UUID
import pytesseract
from PIL import Image
from pathlib import Path
from django.db.utils import IntegrityError

import requests

from .models import Book, Page, Box

prefix = 'lsma'
uri = 'http://scienceandmaterialculture.org/ns/1.0'

etree.register_namespace(prefix, uri)
PdfMetadata.NS[prefix] = uri
PdfMetadata.REVERSE_NS[uri] = prefix


def add_metadata(pdf_path: str, url: str, uuid: UUID) -> None:
    with Pdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        with pdf.open_metadata() as meta:
            meta['lsma:UUID'] = str(uuid)
            meta['lsma:URL'] = url
        pdf.save()
    return

def get_metadata(pdf_path: str) -> UUID:
    with Pdf.open(pdf_path) as pdf:
        with pdf.open_metadata() as meta:
            uuid_str = meta['lsma:UUID']
            uuid = UUID(hex=uuid_str)
            url = meta['lsma:URL']
            return uuid, url


def extract_images(pdf_path, original_folder):
    pdf = Pdf.open(pdf_path)
    if not original_folder.exists():
        original_folder.mkdir()
    for i, page in enumerate(pdf.pages, start=1):
        xobject = page['/Resources']['/XObject']
        for image in xobject.items():
            try:
                image = PdfImage(image[1])
            except TypeError:
                continue
            # might need some logic here to take the largest image on the page
            filename = image.extract_to(fileprefix=f'{original_folder}/{i}')
    pdf.close()

def get_boxes(image_path: str) -> list[list]:
    data = pytesseract.image_to_data(Image.open(image_path))
    data = data.split('\n')
    if data[-1] == '':
        del data[-1]
    data = [line.split('\t') for line in data[1:]]
    return data

def get_stem(path):
    return int(path.stem)

def add_book(pdf_path):
    uuid, url = get_metadata(pdf_path)
    try:
        book = Book.objects.create(uuid=uuid, url=url)
    except IntegrityError:
        raise ValueError('This book is already in the db')
    print(f'Added book {url}')

    original_image_dir = Path(f'original_page_images/{str(uuid)[:8]}')
    extract_images(pdf_path, original_image_dir)

    original_images = sorted(original_image_dir.glob('*'), key=get_stem)

    for original_image in original_images:
        page = Page.objects.create(book=book, original_image=str(original_image), number=int(original_image.stem))
        print('added ', page)
        box_lists = get_boxes(original_image)
        for i, box_list in enumerate(box_lists, start=1):
            box_list.append(i)
            if box_list[10] == -1:
                box_list[10] = None

        page_lists = [Box(
            page=page,
            order=box_list[12],
            level=box_list[0],
            page_number=box_list[1],
            block_number=box_list[2],
            paragraph_number=box_list[3],
            line_number=box_list[4],
            word_number=box_list[5],
            left=box_list[6],
            top=box_list[7],
            width=box_list[8],
            height=box_list[9],
            original_confidence=box_list[10],
            text=box_list[11],
            original_text=box_list[11],
            ) for box_list in box_lists if box_list[0]=='1']
        Box.objects.bulk_create(page_lists)

        block_lists = [Box(
            page=page,
            parent=page_lists[int(box_list[1])-1],
            order=box_list[12],
            level=box_list[0],
            page_number=box_list[1],
            block_number=box_list[2],
            paragraph_number=box_list[3],
            line_number=box_list[4],
            word_number=box_list[5],
            left=box_list[6],
            top=box_list[7],
            width=box_list[8],
            height=box_list[9],
            original_confidence=box_list[10],
            text=box_list[11],
            original_text=box_list[11],
            ) for box_list in box_lists if box_list[0]=='2']
        Box.objects.bulk_create(block_lists)

        paragraph_lists = [Box(
            page=page,
            parent=block_lists[int(box_list[2])-1],
            order=box_list[12],
            level=box_list[0],
            page_number=box_list[1],
            block_number=box_list[2],
            paragraph_number=box_list[3],
            line_number=box_list[4],
            word_number=box_list[5],
            left=box_list[6],
            top=box_list[7],
            width=box_list[8],
            height=box_list[9],
            original_confidence=box_list[10],
            text=box_list[11],
            original_text=box_list[11],
            ) for box_list in box_lists if box_list[0]=='3']
        Box.objects.bulk_create(paragraph_lists)

        line_lists = [Box(
            page=page,
            parent=paragraph_lists[int(box_list[3])-1],
            order=box_list[12],
            level=box_list[0],
            page_number=box_list[1],
            block_number=box_list[2],
            paragraph_number=box_list[3],
            line_number=box_list[4],
            word_number=box_list[5],
            left=box_list[6],
            top=box_list[7],
            width=box_list[8],
            height=box_list[9],
            original_confidence=box_list[10],
            text=box_list[11],
            original_text=box_list[11],
            ) for box_list in box_lists if box_list[0]=='4']
        Box.objects.bulk_create(line_lists)

        word_lists = [Box(
            page=page,
            parent=line_lists[int(box_list[4])-1],
            order=box_list[12],
            level=box_list[0],
            page_number=box_list[1],
            block_number=box_list[2],
            paragraph_number=box_list[3],
            line_number=box_list[4],
            word_number=box_list[5],
            left=box_list[6],
            top=box_list[7],
            width=box_list[8],
            height=box_list[9],
            original_confidence=box_list[10],
            text=box_list[11],
            original_text=box_list[11],
            ) for box_list in box_lists if box_list[0]=='5']
        Box.objects.bulk_create(word_lists)
        page.generate_text()

def remove_book(uuid):
    book = Book.objects.get(uuid=str(uuid))
    book.delete()

def download_url(url: str, new_name: Path) -> None:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(new_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 16*1024):
                f.write(chunk)
