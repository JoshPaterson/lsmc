from django.core.management.base import BaseCommand, CommandError
from lsma.pdf import add_book, add_metadata, download_url
from pathlib import Path
from uuid import uuid4

class Command(BaseCommand):
    help = 'Import urls to pdf directory and import to database'

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str, help='urls that end in .pdf')

    def handle(self, *args, **options):
        pdf_dir = Path('new_pdf_downloads')
        urls = options['urls']
        for url in urls:
            self.stdout.write(f'downloading {url}')
            uuid = uuid4()
            pdf_path = pdf_dir / (str(uuid) + '.pdf')
            download_url(url, pdf_path)
            add_metadata(pdf_path, url, uuid)
            self.stdout.write(f'{url} downloaded')