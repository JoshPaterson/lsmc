from django.core.management.base import BaseCommand, CommandError
from lsma.pdf import add_book
from pathlib import Path
import requests
from uuid import uuid4

def download_url(url: str, new_name: Path) -> None:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(new_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 16*1024):
                f.write(chunk)

class Command(BaseCommand):
    help = 'Import files to database'

    def add_arguments(self, parser):
        parser.add_argument('paths', nargs='+', type=str, help='file paths')

    def handle(self, *args, **options):
        paths = options['paths']
        for pdf_path in paths:
            self.stdout.write(f'importing {pdf_path}')
            try:
                add_book(pdf_path)
            except ValueError:
                raise CommandError('file already in db, use reimport_file command')
            self.stdout.write(f'done with {pdf_path}')