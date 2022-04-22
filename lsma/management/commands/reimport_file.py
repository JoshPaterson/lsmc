from django.core.management.base import BaseCommand, CommandError
from lsma.pdf import add_book, remove_book, get_metadata
from pathlib import Path
import requests
from uuid import uuid4
import shutil

def download_url(url: str, new_name: Path) -> None:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(new_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 16*1024):
                f.write(chunk)

class Command(BaseCommand):
    help = 'Reimport file to database'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+', type=str, help='file paths')

    def handle(self, *args, **options):
        paths = options['paths']
        for pdf_path in paths:
            uuid, _, _= get_metadata(pdf_path)
            original_image_path = Path(f'original_page_images/{str(uuid)[:8]}')
            self.stdout.write(f'removing {pdf_path}')
            remove_book(uuid)
            self.stdout.write(f'deleting previously extracted images for {pdf_path}')
            shutil.rmtree(original_image_path)
            self.stdout.write(f'reimporting {pdf_path}')
            add_book(pdf_path)
            self.stdout.write(f'done with {pdf_path}')