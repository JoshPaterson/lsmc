from cgi import test
import pytest
import pdf_metadata

def test_PdfMetadata():
    pdf = "empty.pdf"

    book = pdf_metadata.PdfMetadata.from_pdf(pdf)
    book.title = "British Mariner's Guide"
    book.authors = ['Maskelyne, Nevil']
    book.edition = 1
    book.date_published = '1763-01-01'
    book.in_copyright = False
    book.write()

if __name__ == '__main__':
    test_PdfMetadata()