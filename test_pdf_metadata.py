import pdf_metadata
import shutil
import tempfile
from pathlib import Path

class temp_copy:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def __enter__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_file_path = self.temp_dir.name + '/' + self.file_path.name
        shutil.copy(self.file_path, self.temp_file_path)
        return self.temp_file_path

    def __exit__(self, exc_type, exc_val, traceback):
        self.temp_dir.cleanup()


def test_PdfMetadata():
    pdf = "empty2.pdf"
    book = pdf_metadata.PdfMetadata.from_pdf(pdf)
    book.title = "British Mariner's Guide"
    book.authors = ['Maskelyne, Nevil']
    book.edition = 1
    book.date_published = '1763-01-01'
    book.in_copyright = False
    book.write()

def test_context_manager():
    with temp_copy('empty_no_metadata.pdf') as f:
        book = pdf_metadata.PdfMetadata.from_pdf(f)
        book.title = 'Sample Title'
        book.authors = []
        book.write()
