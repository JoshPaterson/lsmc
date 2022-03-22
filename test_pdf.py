import pdf
import shutil
import tempfile
from pathlib import Path
import pytest
from pydantic.error_wrappers import ValidationError

from pdf import UNCHECKED

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


class TestPdfIndividualFields():
    def test_url(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.url is pdf.UNCHECKED
            book.url = 'scienceandmaterialculture.com'
            book.write()
            book.url = None
            book.write()
            with pytest.raises(ValidationError):
                book.url = []

    def test_authors(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.authors is pdf.UNCHECKED
            book.authors = ['Makelyne, Nevil', 'Bowditch, Nathaniel']
            book.write()
            book.authors = []
            book.write()
            with pytest.raises(ValidationError):
                book.authors = 'Maskelyne, Nevil'

    def test_editors(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.editors is pdf.UNCHECKED
            book.editors= ['Makelyne, Nevil', 'Bowditch, Nathaniel']
            book.write()
            book.editors= []
            book.write()
            with pytest.raises(ValidationError):
                book.editors= 'Maskelyne, Nevil'

    def test_translators(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.translators is pdf.UNCHECKED
            book.translators = ['Makelyne, Nevil', 'Bowditch, Nathaniel']
            book.write()
            book.translators= []
            book.write()
            with pytest.raises(ValidationError):
                book.translators= 'Maskelyne, Nevil'

    def test_date_published(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.date_published is pdf.UNCHECKED
            book.date_published = '1763-01-01'
            book.write()
            book.date_published = 1763
            book.write()
            book.date_published = None
            book.write()
            with pytest.raises(ValidationError):
                book.date_published = []

    def test_publishing_frequency(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.publishing_frequency is pdf.UNCHECKED
            book.publishing_frequency = 'monthly'
            book.write()
            book.publishing_frequency = None
            book.write()
            with pytest.raises(ValidationError):
                book.publishing_frequency = []

    def test_title(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.title is pdf.UNCHECKED
            book.title = "British Mariner's Guide"
            book.write()
            book.title = None
            book.write()
            with pytest.raises(ValidationError):
                book.title = []

    def test_subtitle(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.subtitle is pdf.UNCHECKED
            book.subtitle = "British Mariner's Guide"
            book.write()
            book.subtitle = None
            book.write()
            with pytest.raises(ValidationError):
                book.subtitle = []

    def test_long_title(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.long_title is pdf.UNCHECKED
            book.long_title = "British Mariner's Guide"
            book.write()
            book.long_title = None
            book.write()
            with pytest.raises(ValidationError):
                book.long_title = []

    def test_edition(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.edition is pdf.UNCHECKED
            book.edition = 1
            book.write()
            book.edition = None
            book.write()
            with pytest.raises(ValidationError):
                book.edition = []

    def test_volume(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.volume is pdf.UNCHECKED
            book.volume = 2
            book.write()
            book.volume = None
            book.write()
            with pytest.raises(ValidationError):
                book.volume = []

    def test_in_copyright(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.in_copyright is pdf.UNCHECKED
            book.in_copyright = True
            book.write()
            book.in_copyright = None
            book.write()
            with pytest.raises(ValidationError):
                book.in_copyright = []

    def test_copyright_years(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.copyright_years is pdf.UNCHECKED
            book.copyright_years = [1752, 1758, 1762]
            book.write()
            book.copyright_years = []
            book.write()
            with pytest.raises(ValidationError):
                book.copyright_years = 'test'

    def test_publishers(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.publishers is pdf.UNCHECKED
            book.publishers = ['test', 'test1']
            book.write()
            book.publishers = []
            book.write()
            with pytest.raises(ValidationError):
                book.publishers = 'test'

    def test_publisher_cities(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.publisher_cities is pdf.UNCHECKED
            book.publisher_cities = ['test', 'test2']
            book.write()
            book.publisher_cities = []
            book.write()
            with pytest.raises(ValidationError):
                book.publisher_cities = 'test'

    def test_printers(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.printers is pdf.UNCHECKED
            book.printers = ['test', 'test2']
            book.write()
            book.printers = []
            book.write()
            with pytest.raises(ValidationError):
                book.printers = 'test'

    def test_printing_number(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.printing_number is pdf.UNCHECKED
            book.printing_number = 2
            book.write()
            book.printing_number = None
            book.write()
            with pytest.raises(ValidationError):
                book.printing_number = []

    def test_numbers_offset(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.numbers_offset is pdf.UNCHECKED
            book.numbers_offset = 12
            book.write()
            book.numbers_offset = None
            book.write()
            with pytest.raises(ValidationError):
                book.numbers_offset = []

    def test_roman_numbers_offset(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.roman_numbers_offset is pdf.UNCHECKED
            book.roman_numbers_offset = 5
            book.write()
            book.roman_numbers_offset = None
            book.write()
            with pytest.raises(ValidationError):
                book.roman_numbers_offset = []

    def test_has_ligatures(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.has_ligatures is pdf.UNCHECKED
            book.has_ligatures = True
            book.write()
            with pytest.raises(ValidationError):
                book.has_ligatures = []

    def test_book_topics(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.book_topics is pdf.UNCHECKED
            book.book_topics = ['Navigation', 'Astronomy']
            book.write()
            book.book_topics = []
            book.write()
            with pytest.raises(ValidationError):
                book.book_topics = 'test'

    def test_blank_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.blank_pages is pdf.UNCHECKED
            book.blank_pages = [1,2,3]
            book.write()
            book.blank_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.blank_pages = 1

    def test_title_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.title_pages is pdf.UNCHECKED
            book.title_pages = [1,2,3]
            book.write()
            book.title_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.title_pages = 1

    def test_publishing_info_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.publishing_info_pages is pdf.UNCHECKED
            book.publishing_info_pages = [1,2,3]
            book.write()
            book.publishing_info_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.publishing_info_pages = 1

    def test_front_cover_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.front_cover_pages is pdf.UNCHECKED
            book.front_cover_pages = [1,2,3]
            book.write()
            book.front_cover_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.front_cover_pages = 1

    def test_back_cover_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.back_cover_pages is pdf.UNCHECKED
            book.back_cover_pages = [1,2,3]
            book.write()
            book.back_cover_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.back_cover_pages = 1

    def test_end_paper_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.end_paper_pages is pdf.UNCHECKED
            book.end_paper_pages = [1,2,3]
            book.write()
            book.end_paper_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.end_paper_pages = 1

    def test_printing_info_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.printing_info_pages is pdf.UNCHECKED
            book.printing_info_pages = [1,2,3]
            book.write()
            book.printing_info_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.printing_info_pages = 1

    def test_half_title_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.half_title_pages is pdf.UNCHECKED
            book.half_title_pages = [1,2,3]
            book.write()
            book.half_title_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.half_title_pages = 1

    def test_frontispiece_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.frontispiece_pages is pdf.UNCHECKED
            book.frontispiece_pages = [1,2,3]
            book.write()
            book.frontispiece_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.frontispiece_pages = 1

    def test_illustration_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.illustration_pages is pdf.UNCHECKED
            book.illustration_pages = [1,2,3]
            book.write()
            book.illustration_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.illustration_pages = 1

    def test_advertisement_partial_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.advertisement_partial_pages is pdf.UNCHECKED
            book.advertisement_partial_pages = [1,2,3]
            book.write()
            book.advertisement_partial_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.advertisement_partial_pages = 1

    def test_advertisement_full_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.advertisement_full_pages is pdf.UNCHECKED
            book.advertisement_full_pages = [1,2,3]
            book.write()
            book.advertisement_full_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.advertisement_full_pages = 1

    def test_photograph_pages(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            assert book.photograph_pages is pdf.UNCHECKED
            book.photograph_pages = [1,2,3]
            book.write()
            book.photograph_pages = []
            book.write()
            with pytest.raises(ValidationError):
                book.photograph_pages = 1


class TestSignatureIndividualFields:
    def test_page(self):
        signature = pdf.Signature(**{'Page':16})
        signature.page = 24
        with pytest.raises(ValidationError):
            signature.page = []

    def test_name(self):
        signature = pdf.Signature(**{'Page':16})
        assert signature.name is pdf.UNCHECKED
        signature.name = 'A'
        with pytest.raises(ValidationError):
            signature.name = []


class TestPlateIndividualFields:
    def test_number(self):
        plate = pdf.Plate(**{'Pages':[1,2,3]})
        assert plate.number is pdf.UNCHECKED
        plate.number = 3
        with pytest.raises(ValidationError):
            plate.number = []

    def test_number_kind(self):
        plate = pdf.Plate(**{'Pages':[1,2,3]})
        assert plate.number_kind is pdf.UNCHECKED
        plate.number_kind = 'arabic'
        with pytest.raises(ValidationError):
            plate.number_kind = 'test'

    def test_pages(self):
        plate = pdf.Plate(**{'Pages':[1,2,3]})
        plate.pages.append(4)
        with pytest.raises(ValidationError):
            plate.pages = 3


class TestSectionIndividualFields:
    def test_kind(self):
        pass

    def test_kind_in_book(self):
        pass

    def test_title(self):
        pass

    def test_authors(self):
        pass

    def test_number(self):
        pass

    def test_number_kind(self):
        pass

    def test_for_edition(self):
        pass

    def test_heading_page(self):
        pass

    def test_first_page(self):
        pass

    def test_last_page(self):
        pass

    def test_topics(self):
        pass
