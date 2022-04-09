from pikepdf import Pdf, PdfImage
from pikepdf.models.metadata import PdfMetadata
from lxml import etree
from uuid import UUID, uuid4
import pytesseract
from PIL import Image
import hunspell
dictionary = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
import string
import re
from pathlib import Path
regex = re.compile(f'[{re.escape(string.punctuation)}]')
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

def make_word_list(data: list[list]):
    words = [line[-1].lower() for line in data if line[-1] != '']
    words_no_hyphen = []
    skip = False
    for word in words:
        if skip:
            words_no_hyphen[-1] = words_no_hyphen[-1] + word
            skip = False
            continue
        if word[-1] != '-':
            words_no_hyphen.append(word)
        else:
            words_no_hyphen.append(word[:-1])
            skip = True
    words = [regex.sub('', word) for word in words_no_hyphen]
    return [word for word in words if word != '']


def fix_long_s(word):
    if dictionary.spell(word):
        return word
    elif dictionary.spell(word.replace('f', 's')):
        return word.replace('f', 's')
    else:
        return word

def clean_words_long_s(words):
    return [fix_long_s(word) for word in words]

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
        Box.objects.bulk_create(
            [Box(
            page=page,
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
            ) for box_list in box_lists]
        )

def remove_book(uuid):
    book = Book.objects.get(uuid=str(uuid))
    book.delete()

def download_url(url: str, new_name: Path) -> None:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(new_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 16*1024):
                f.write(chunk)
