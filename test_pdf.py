import pdf
import shutil
import tempfile
from pathlib import Path
import pytest
from pydantic.error_wrappers import ValidationError

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


class TestPdfFields():
    def test_url(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.url is pdf.UNCHECKED
        book.url = 'scienceandmaterialculture.com'
        book.url = None
        with pytest.raises(ValidationError):
            book.url = []

    def test_authors(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.authors is pdf.UNCHECKED
        book.authors = ['Makelyne, Nevil', 'Bowditch, Nathaniel']
        book.authors = []
        with pytest.raises(ValidationError):
            book.authors = 'Maskelyne, Nevil'

    def test_editors(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.editors is pdf.UNCHECKED
        book.editors= ['Makelyne, Nevil', 'Bowditch, Nathaniel']
        book.editors= []
        with pytest.raises(ValidationError):
            book.editors= 'Maskelyne, Nevil'

    def test_translators(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.translators is pdf.UNCHECKED
        book.translators = ['Makelyne, Nevil', 'Bowditch, Nathaniel']
        book.translators= []
        with pytest.raises(ValidationError):
            book.translators= 'Maskelyne, Nevil'

    def test_date_published(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.date_published is pdf.UNCHECKED
        book.date_published = '1763-01-01'
        book.date_published = 1763
        book.date_published = None
        with pytest.raises(ValidationError):
            book.date_published = []

    def test_publishing_frequency(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publishing_frequency is pdf.UNCHECKED
        book.publishing_frequency = 'monthly'
        book.publishing_frequency = None
        with pytest.raises(ValidationError):
            book.publishing_frequency = []

    def test_title(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.title is pdf.UNCHECKED
        book.title = "British Mariner's Guide"
        book.title = None
        with pytest.raises(ValidationError):
            book.title = []

    def test_subtitle(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.subtitle is pdf.UNCHECKED
        book.subtitle = "British Mariner's Guide"
        book.subtitle = None
        with pytest.raises(ValidationError):
            book.subtitle = []

    def test_long_title(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.long_title is pdf.UNCHECKED
        book.long_title = "British Mariner's Guide"
        book.long_title = None
        with pytest.raises(ValidationError):
            book.long_title = []

    def test_edition(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.edition is pdf.UNCHECKED
        book.edition = 1
        book.edition = None
        with pytest.raises(ValidationError):
            book.edition = []

    def test_volume(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.volume is pdf.UNCHECKED
        book.volume = 2
        book.volume = None
        with pytest.raises(ValidationError):
            book.volume = []

    def test_in_copyright(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.in_copyright is pdf.UNCHECKED
        book.in_copyright = True
        book.in_copyright = None
        with pytest.raises(ValidationError):
            book.in_copyright = []

    def test_copyright_years(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.copyright_years is pdf.UNCHECKED
        book.copyright_years = [1752, 1758, 1762]
        book.copyright_years = []
        with pytest.raises(ValidationError):
            book.copyright_years = 'test'

    def test_publishers(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publishers is pdf.UNCHECKED
        book.publishers = ['test', 'test1']
        book.publishers = []
        with pytest.raises(ValidationError):
            book.publishers = 'test'

    def test_publisher_cities(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publisher_cities is pdf.UNCHECKED
        book.publisher_cities = ['test', 'test2']
        book.publisher_cities = []
        with pytest.raises(ValidationError):
            book.publisher_cities = 'test'

    def test_printers(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.printers is pdf.UNCHECKED
        book.printers = ['test', 'test2']
        book.printers = []
        with pytest.raises(ValidationError):
            book.printers = 'test'

    def test_printing_number(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.printing_number is pdf.UNCHECKED
        book.printing_number = 2
        book.printing_number = None
        with pytest.raises(ValidationError):
            book.printing_number = []

    def test_numbers_offset(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.numbers_offset is pdf.UNCHECKED
        book.numbers_offset = 12
        book.numbers_offset = None
        with pytest.raises(ValidationError):
            book.numbers_offset = []

    def test_roman_numbers_offset(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
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
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.has_ligatures is pdf.UNCHECKED
        book.has_ligatures = True
        with pytest.raises(ValidationError):
            book.has_ligatures = []

    def test_book_topics(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.book_topics is pdf.UNCHECKED
        book.book_topics = ['Navigation', 'Astronomy']
        book.book_topics = []
        with pytest.raises(ValidationError):
            book.book_topics = 'test'

    def test_blank_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.blank_pages is pdf.UNCHECKED
        book.blank_pages = [1,2,3]
        book.blank_pages = []
        with pytest.raises(ValidationError):
            book.blank_pages = 1

    def test_title_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.title_pages is pdf.UNCHECKED
        book.title_pages = [1,2,3]
        book.title_pages = []
        with pytest.raises(ValidationError):
            book.title_pages = 1

    def test_publishing_info_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publishing_info_pages is pdf.UNCHECKED
        book.publishing_info_pages = [1,2,3]
        book.publishing_info_pages = []
        with pytest.raises(ValidationError):
            book.publishing_info_pages = 1

    def test_front_cover_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.front_cover_pages is pdf.UNCHECKED
        book.front_cover_pages = [1,2,3]
        book.front_cover_pages = []
        with pytest.raises(ValidationError):
            book.front_cover_pages = 1

    def test_back_cover_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.back_cover_pages is pdf.UNCHECKED
        book.back_cover_pages = [1,2,3]
        book.back_cover_pages = []
        with pytest.raises(ValidationError):
            book.back_cover_pages = 1

    def test_end_paper_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.end_paper_pages is pdf.UNCHECKED
        book.end_paper_pages = [1,2,3]
        book.end_paper_pages = []
        with pytest.raises(ValidationError):
            book.end_paper_pages = 1

    def test_printing_info_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.printing_info_pages is pdf.UNCHECKED
        book.printing_info_pages = [1,2,3]
        book.printing_info_pages = []
        with pytest.raises(ValidationError):
            book.printing_info_pages = 1

    def test_half_title_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.half_title_pages is pdf.UNCHECKED
        book.half_title_pages = [1,2,3]
        book.half_title_pages = []
        with pytest.raises(ValidationError):
            book.half_title_pages = 1

    def test_frontispiece_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.frontispiece_pages is pdf.UNCHECKED
        book.frontispiece_pages = [1,2,3]
        book.frontispiece_pages = []
        with pytest.raises(ValidationError):
            book.frontispiece_pages = 1

    def test_illustration_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.illustration_pages is pdf.UNCHECKED
        book.illustration_pages = [1,2,3]
        book.illustration_pages = []
        with pytest.raises(ValidationError):
            book.illustration_pages = 1

    def test_advertisement_partial_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.advertisement_partial_pages is pdf.UNCHECKED
        book.advertisement_partial_pages = [1,2,3]
        book.advertisement_partial_pages = []
        with pytest.raises(ValidationError):
            book.advertisement_partial_pages = 1

    def test_advertisement_full_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.advertisement_full_pages is pdf.UNCHECKED
        book.advertisement_full_pages = [1,2,3]
        book.advertisement_full_pages = []
        with pytest.raises(ValidationError):
            book.advertisement_full_pages = 1

    def test_photograph_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.photograph_pages is pdf.UNCHECKED
        book.photograph_pages = [1,2,3]
        book.photograph_pages = []
        with pytest.raises(ValidationError):
            book.photograph_pages = 1

    def test_sections(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34,
                          'Sections': [
                              {'FirstPage': 1, 'LastPage': 5},
                              {'FirstPage': 6, 'LastPage': 10}]
                        })
        book.sections = []
        with pytest.raises(ValidationError):
            book.sections = 'test'

    def test_plates(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34,
                          'Plates': [
                              {'Pages': [5, 6]},
                              {'Pages': [7, 8]}]
                        })
        book.plates= []
        with pytest.raises(ValidationError):
            book.plates = 'test'

    def test_signatures(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34,
                          'Signatures': [
                              {'Page': 16},
                              {'Page': 32}]
                        })
        book.signatures = []
        with pytest.raises(ValidationError):
            book.signatures = 'test'


class TestSignatureFields:
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


class TestPlateFields:
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


class TestSectionFields:
    def test_kind(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.kind is pdf.UNCHECKED
        section.kind = 'introduction'
        with pytest.raises(ValidationError):
            section.kind = None
        with pytest.raises(ValidationError):
            section.kind = 'test'

    def test_kind_in_book(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.kind_in_book is pdf.UNCHECKED
        section.kind_in_book = 'chapter'
        with pytest.raises(ValidationError):
            section.kind_in_book = None
        with pytest.raises(ValidationError):
            section.kind_in_book = []

    def test_title(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.title is pdf.UNCHECKED
        section.title = 'Basics of Trigonometry'
        section.title = None
        with pytest.raises(ValidationError):
            section.title = []

    def test_authors(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.authors is pdf.UNCHECKED
        section.authors = ['Maskelyne, Nevil']
        with pytest.raises(ValidationError):
            section.authors = 'test'

    def test_number(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.number is pdf.UNCHECKED
        section.number = 4
        section.number = None
        with pytest.raises(ValidationError):
            section.number = 'test'

    def test_number_kind(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.number_kind is pdf.UNCHECKED
        section.number_kind = 'arabic'
        section.number_kind = None
        with pytest.raises(ValidationError):
            section.number_kind = 'test'

    def test_for_edition(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.for_edition is pdf.UNCHECKED
        section.for_edition = 2
        section.for_edition = None
        with pytest.raises(ValidationError):
            section.for_edition = 'test'

    def test_heading_page(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 4})
        assert section.heading_page is pdf.UNCHECKED
        section.heading_page = 2
        with pytest.raises(ValidationError):
            section.heading_page = 5
        with pytest.raises(ValidationError):
            section.heading_page = None
        with pytest.raises(ValidationError):
            section.heading_page = 'test'

    def test_first_page(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 3})
        section.first_page = 2
        with pytest.raises(ValidationError):
            section.first_page = 4
        with pytest.raises(ValidationError):
            section.first_page = 'test'

    def test_last_page(self):
        with pytest.raises(ValidationError):
            section = pdf.Section(**{'FirstPage': 2, 'LastPage': 1})
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 3})
        section.last_page = 2
        with pytest.raises(ValidationError):
            section.last_page = 'test'

    def test_topics(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.topics is pdf.UNCHECKED
        section.topics = ['Navigation', 'Trigonometry']
        section.topics = []
        with pytest.raises(ValidationError):
            section.topics = 'test'


class TestReadWrite:
    def test_all_unchecked(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)


    def test_all_null(self):
        pass

    def test_all_values(self):
        pass