from django.core.management.base import BaseCommand, CommandError
from lsma.pdf import add_book, add_metadata, download_url
from pathlib import Path
from uuid import uuid4
import shutil

class Command(BaseCommand):
    help = 'Copy local files to pdf directory'

    def add_arguments(self, parser):
        parser.add_argument('files', nargs='+', type=str, help='urls that end in .pdf')

    def handle(self, *args, **options):
        pdf_dir = Path('new_pdf_downloads')
        files = options['files']
        for f in files:
            f = Path(f)
            if f.suffix not in ['.pdf', '.PDF']:
                raise ValueError('file is not a pdf file')
            self.stdout.write(f'copying {f}')
            uuid = uuid4()
            pdf_path = pdf_dir / (str(uuid) + '.pdf')
            shutil.copy(f, pdf_path)
            add_metadata(pdf_path, '', uuid)
            self.stdout.write(f'{f} copied')