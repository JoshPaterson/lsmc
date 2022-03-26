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
        assert book.url == pdf.UNCHECKED
        v = 'scienceandmaterialculture.com'
        book.url = v
        assert book.url == v
        book.url = None
        assert book.url == None
        book.url = pdf.UNCHECKED
        assert book.url == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.url = []

    def test_authors(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.authors == pdf.UNCHECKED
        v = ['Makelyne, Nevil', 'Bowditch, Nathaniel']
        book.authors = v
        assert book.authors == v
        book.authors = []
        assert book.authors == []
        book.authors = pdf.UNCHECKED
        assert book.authors == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.authors = None
        with pytest.raises(ValidationError):
            book.authors = 'Maskelyne, Nevil'

    def test_editors(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.editors == pdf.UNCHECKED
        v = ['Makelyne, Nevil', 'Bowditch, Nathaniel']
        book.editors = v
        assert book.editors == v
        book.editors = []
        assert book.editors == []
        book.editors = pdf.UNCHECKED
        assert book.editors == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.editors = None
        with pytest.raises(ValidationError):
            book.editors = 'Maskelyne, Nevil'

    def test_translators(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.translators == pdf.UNCHECKED
        v = ['Makelyne, Nevil', 'Bowditch, Nathaniel']
        book.translators = v
        assert book.translators == v
        book.translators = []
        assert book.translators == []
        book.translators= pdf.UNCHECKED
        assert book.translators== pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.translators= None
        with pytest.raises(ValidationError):
            book.translators = 'Maskelyne, Nevil'

    def test_date_published(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.date_published == pdf.UNCHECKED
        v = '1763-01-01'
        book.date_published = v
        assert book.date_published == v
        book.date_published = 1763
        assert book.date_published == v
        book.date_published = None
        assert book.date_published == None
        book.date_published = pdf.UNCHECKED
        assert book.date_published == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.date_published = []

    def test_publishing_frequency(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publishing_frequency == pdf.UNCHECKED
        v = 'monthly'
        book.publishing_frequency = v
        assert book.publishing_frequency == v
        book.publishing_frequency = None
        assert book.publishing_frequency == None
        book.publishing_frequency = pdf.UNCHECKED
        assert book.publishing_frequency == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.publishing_frequency = []

    def test_title(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.title == pdf.UNCHECKED
        v = "British Mariner's Guide"
        book.title = v
        assert book.title == v
        book.title = None
        assert book.title == None
        book.title = pdf.UNCHECKED
        assert book.title == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.title = []

    def test_subtitle(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.subtitle == pdf.UNCHECKED
        v = "British Mariner's Guide"
        book.subtitle = v
        assert book.subtitle == v
        book.subtitle = None
        assert book.subtitle == None
        book.subtitle = pdf.UNCHECKED
        assert book.subtitle == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.subtitle = []

    def test_long_title(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.long_title == pdf.UNCHECKED
        v = "British Mariner's Guide"
        book.long_title = v
        assert book.long_title == v
        book.long_title = None
        assert book.long_title == None
        book.long_title = pdf.UNCHECKED
        assert book.long_title == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.long_title = []

    def test_edition(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.edition == pdf.UNCHECKED
        v = 1
        book.edition = v
        assert book.edition == v
        book.edition = None
        assert book.edition == None
        book.edition = pdf.UNCHECKED
        assert book.edition == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.edition = []

    def test_volume(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.volume == pdf.UNCHECKED
        v = 2
        book.volume = v
        assert book.volume == v
        book.volume = None
        assert book.volume == None
        book.volume = pdf.UNCHECKED
        assert book.volume == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.volume = []

    def test_in_copyright(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.in_copyright == pdf.UNCHECKED
        v = True
        book.in_copyright = v
        assert book.in_copyright == v
        book.in_copyright = None
        assert book.in_copyright == None
        book.in_copyright = pdf.UNCHECKED
        assert book.in_copyright == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.in_copyright = []

    def test_copyright_years(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.copyright_years == pdf.UNCHECKED
        v = [1752, 1758, 1762]
        book.copyright_years = v
        assert book.copyright_years == v
        book.copyright_years = []
        assert book.copyright_years == []
        book.copyright_years = pdf.UNCHECKED
        assert book.copyright_years == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.copyright_years = 'test'

    def test_publishers(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publishers == pdf.UNCHECKED
        v = ['test', 'test1']
        book.publishers = v
        assert book.publishers == v
        book.publishers = []
        assert book.publishers == []
        book.publishers = pdf.UNCHECKED
        assert book.publishers == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.publishers = 'test'

    def test_publisher_cities(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publisher_cities == pdf.UNCHECKED
        v = ['test', 'test2']
        book.publisher_cities = v
        assert book.publisher_cities == v
        book.publisher_cities = []
        assert book.publisher_cities == []
        book.publisher_cities = pdf.UNCHECKED
        assert book.publisher_cities == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.publisher_cities = 'test'

    def test_printers(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.printers == pdf.UNCHECKED
        v = ['test', 'test2']
        book.printers = v
        assert book.printers == v
        book.printers = []
        assert book.printers == []
        book.printers = pdf.UNCHECKED
        assert book.printers == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.printers = 'test'

    def test_printing_number(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.printing_number == pdf.UNCHECKED
        v = 2
        book.printing_number = v
        assert book.printing_number == v
        book.printing_number = None
        assert book.printing_number == None
        book.printing_number = pdf.UNCHECKED
        assert book.printing_number == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.printing_number = []

    def test_numbers_offset(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.numbers_offset == pdf.UNCHECKED
        v = 12
        book.numbers_offset = v
        assert book.numbers_offset == v
        book.numbers_offset = None
        assert book.numbers_offset == None
        book.numbers_offset = pdf.UNCHECKED
        assert book.numbers_offset == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.numbers_offset = []

    def test_roman_numbers_offset(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.roman_numbers_offset == pdf.UNCHECKED
        v = 5
        book.roman_numbers_offset = v
        assert book.roman_numbers_offset == v
        book.roman_numbers_offset = None
        assert book.roman_numbers_offset == None
        book.roman_numbers_offset = pdf.UNCHECKED
        assert book.roman_numbers_offset == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.roman_numbers_offset = []

    def test_has_ligatures(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.has_ligatures == pdf.UNCHECKED
        book.has_ligatures = True
        assert book.has_ligatures == True
        book.has_ligatures = pdf.UNCHECKED
        assert book.has_ligatures == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.has_ligatures = []

    def test_book_topics(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.book_topics == pdf.UNCHECKED
        v = ['Navigation', 'Astronomy']
        book.book_topics = v
        assert book.book_topics == v
        book.book_topics = []
        assert book.book_topics == []
        book.book_topics = pdf.UNCHECKED
        assert book.book_topics == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.book_topics = 'test'

    def test_blank_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.blank_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.blank_pages = v
        assert book.blank_pages == v
        book.blank_pages = []
        assert book.blank_pages == []
        book.blank_pages = pdf.UNCHECKED
        assert book.book_topics == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.blank_pages = 1

    def test_title_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.title_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.title_pages = v
        assert book.title_pages == v
        book.title_pages = []
        assert book.title_pages == []
        book.title_pages = pdf.UNCHECKED
        assert book.title_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.title_pages = 1

    def test_publishing_info_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.publishing_info_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.publishing_info_pages = v
        assert book.publishing_info_pages == v
        book.publishing_info_pages = []
        assert book.publishing_info_pages == []
        book.publishing_info_pages = pdf.UNCHECKED
        assert book.publishing_info_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.publishing_info_pages = 1

    def test_front_cover_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.front_cover_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.front_cover_pages = v
        assert book.front_cover_pages == v
        book.front_cover_pages = []
        assert book.front_cover_pages == []
        book.front_cover_pages = pdf.UNCHECKED
        assert book.front_cover_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.front_cover_pages = 1

    def test_back_cover_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.back_cover_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.back_cover_pages = v
        assert book.back_cover_pages == v
        book.back_cover_pages = []
        assert book.back_cover_pages == []
        book.back_cover_pages = pdf.UNCHECKED
        assert book.back_cover_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.back_cover_pages = 1

    def test_end_paper_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.end_paper_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.end_paper_pages = v
        assert book.end_paper_pages == v
        book.end_paper_pages = []
        assert book.end_paper_pages == []
        book.end_paper_pages= pdf.UNCHECKED
        assert book.end_paper_pages== pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.end_paper_pages = 1

    def test_printing_info_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.printing_info_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.printing_info_pages = v
        assert book.printing_info_pages == v
        book.printing_info_pages = []
        assert book.printing_info_pages == []
        book.printing_info_pages = pdf.UNCHECKED
        assert book.printing_info_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.printing_info_pages = 1

    def test_half_title_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.half_title_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.half_title_pages = v
        assert book.half_title_pages == v
        book.half_title_pages = []
        assert book.half_title_pages == []
        book.half_title_pages = pdf.UNCHECKED
        assert book.half_title_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.half_title_pages = 1

    def test_frontispiece_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.frontispiece_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.frontispiece_pages = v
        assert book.frontispiece_pages == v
        book.frontispiece_pages = []
        assert book.frontispiece_pages == []
        book.frontispiece_pages = pdf.UNCHECKED
        assert book.frontispiece_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.frontispiece_pages = 1

    def test_illustration_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.illustration_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.illustration_pages = v
        assert book.illustration_pages == v
        book.illustration_pages = []
        assert book.illustration_pages == []
        book.illustration_pages = pdf.UNCHECKED
        assert book.illustration_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.illustration_pages = 1

    def test_advertisement_partial_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.advertisement_partial_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.advertisement_partial_pages = v
        assert book.advertisement_partial_pages == v
        book.advertisement_partial_pages = []
        assert book.advertisement_partial_pages == []
        book.advertisement_partial_pages = pdf.UNCHECKED
        assert book.advertisement_partial_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.advertisement_partial_pages = 1

    def test_advertisement_full_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.advertisement_full_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.advertisement_full_pages = v
        assert book.advertisement_full_pages == v
        book.advertisement_full_pages = []
        assert book.advertisement_full_pages == []
        book.advertisement_full_pages = pdf.UNCHECKED
        assert book.advertisement_full_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.advertisement_full_pages = 1

    def test_photograph_pages(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.photograph_pages == pdf.UNCHECKED
        v = [1,2,3]
        book.photograph_pages = v
        assert book.photograph_pages == v
        book.photograph_pages = []
        assert book.photograph_pages == []
        book.photograph_pages = pdf.UNCHECKED
        assert book.photograph_pages == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.photograph_pages = 1

    def test_sections(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34})
        book.sections = [pdf.Section(**{'FirstPage': 1, 'LastPage': 5}),
                         pdf.Section(**{'FirstPage': 6, 'LastPage': 10})]
        assert book.sections[0].first_page == 1
        assert book.sections[0].last_page == 5
        assert book.sections[1].first_page == 6
        assert book.sections[1].last_page == 10
        book.sections = []
        assert book.sections == []
        book.sections = pdf.UNCHECKED
        assert book.sections == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.sections = 'test'

    def test_plates(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34})
        book.plates = [pdf.Plate(**{'Pages': [5, 6]}),
                       pdf.Plate(**{'Pages': [7, 8]})]
        assert book.plates[0].pages == [5, 6]
        assert book.plates[1].pages == [7, 8]
        book.plates = []
        assert book.plates == []
        book.plates = pdf.UNCHECKED
        assert book.plates == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.plates = 'test'

    def test_signatures(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34})
        book.signatures = [pdf.Signature(**{'Page': 16}),
                           pdf.Signature(**{'Page': 32})]
        assert book.signatures[0].page == 16
        assert book.signatures[1].page == 32
        book.signatures = []
        assert book.signatures == []
        book.signatures = pdf.UNCHECKED
        assert book.signatures == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.signatures = 'test'


class TestSignatureFields:
    def test_page(self):
        signature = pdf.Signature(**{'Page':16})
        assert signature.page == 16
        signature.page = 24
        assert signature.page == 24
        with pytest.raises(ValidationError):
            signature.page = pdf.UNCHECKED
        with pytest.raises(ValidationError):
            signature.page = []

    def test_name(self):
        signature = pdf.Signature(**{'Page':16})
        assert signature.name == pdf.UNCHECKED
        v = 'A'
        signature.name = v
        assert signature.name == v
        signature.name = pdf.UNCHECKED
        assert signature.name == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            signature.name = []


class TestPlateFields:
    def test_number(self):
        plate = pdf.Plate(**{'Pages':[1,2,3]})
        assert plate.number == pdf.UNCHECKED
        v = 3
        plate.number = v
        assert plate.number == v
        plate.number = None
        assert plate.number == None
        plate.number = pdf.UNCHECKED
        assert plate.number == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            plate.number = []

    def test_number_kind(self):
        plate = pdf.Plate(**{'Pages':[1,2,3]})
        assert plate.number_kind == pdf.UNCHECKED
        v = 'arabic'
        plate.number_kind = v
        assert plate.number_kind == v
        plate.number_kind = None
        assert plate.number_kind == None
        plate.number_kind = pdf.UNCHECKED
        assert plate.number_kind == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            plate.number_kind = 'test'

    def test_pages(self):
        plate = pdf.Plate(**{'Pages':[1,2,3]})
        assert plate.pages == [1, 2, 3]
        plate.pages.append(4)
        assert plate.pages == [1, 2, 3, 4]
        with pytest.raises(ValidationError):
            plate.pages = []
        with pytest.raises(ValidationError):
            plate.pages = None
        with pytest.raises(ValidationError):
            plate.pages = pdf.UNCHECKED
        with pytest.raises(ValidationError):
            plate.pages = 3


class TestSectionFields:
    def test_kind(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.kind == pdf.UNCHECKED
        v = 'introduction'
        section.kind = v
        assert section.kind == v
        section.kind = pdf.UNCHECKED
        assert section.kind == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.kind = None
        with pytest.raises(ValidationError):
            section.kind = 'test'

    def test_kind_in_book(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.kind_in_book == pdf.UNCHECKED
        v = 'chapter'
        section.kind_in_book = v
        assert section.kind_in_book == v
        section.kind_in_book = pdf.UNCHECKED
        assert section.kind_in_book == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.kind_in_book = None
        with pytest.raises(ValidationError):
            section.kind_in_book = []

    def test_title(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.title == pdf.UNCHECKED
        v = 'Basics of Trigonometry'
        section.title = v
        assert section.title == v
        section.title = None
        assert section.title == None
        section.title = pdf.UNCHECKED
        assert section.title == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.title = []

    def test_authors(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.authors == pdf.UNCHECKED
        v = ['Maskelyne, Nevil']
        section.authors = v
        assert section.authors == v
        section.authors = []
        assert section.authors == []
        section.authors = pdf.UNCHECKED
        assert section.authors == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.authors = None
        with pytest.raises(ValidationError):
            section.authors = 'test'

    def test_number(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.number == pdf.UNCHECKED
        v = 4
        section.number = v
        assert section.number == v
        section.number = None
        assert section.number == None
        section.number = pdf.UNCHECKED
        assert section.number == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.number = 'test'

    def test_number_kind(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.number_kind == pdf.UNCHECKED
        v = 'arabic'
        section.number_kind = v
        assert section.number_kind == v
        section.number_kind = None
        assert section.number_kind == None
        section.number_kind = pdf.UNCHECKED
        assert section.number_kind == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.number_kind = 'test'

    def test_for_edition(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.for_edition == pdf.UNCHECKED
        v = 2
        section.for_edition = v
        assert section.for_edition == v
        section.for_edition = None
        assert section.for_edition == None
        section.for_edition = pdf.UNCHECKED
        assert section.for_edition == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.for_edition = 'test'

    def test_heading_page(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 4})
        assert section.heading_page == pdf.UNCHECKED
        v = 2
        section.heading_page = v
        assert section.heading_page == v
        section.heading_page = pdf.UNCHECKED
        assert section.heading_page == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.heading_page = 5
        with pytest.raises(ValidationError):
            section.heading_page = None
        with pytest.raises(ValidationError):
            section.heading_page = 'test'

    def test_first_page(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 3})
        v = 2
        section.first_page = v
        assert section.first_page == v
        with pytest.raises(ValidationError):
            section.first_page = pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.first_page = None
        with pytest.raises(ValidationError):
            section.first_page = 4
        with pytest.raises(ValidationError):
            section.first_page = 'test'

    def test_last_page(self):
        with pytest.raises(ValidationError):
            section = pdf.Section(**{'FirstPage': 2, 'LastPage': 1})
        section = pdf.Section(**{'FirstPage': 2, 'LastPage': 4})
        assert section.last_page == 4
        v = 2
        section.last_page = v
        assert section.last_page == v
        with pytest.raises(ValidationError):
            section.first_page = pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.last_page = None
        with pytest.raises(ValidationError):
            section.last_page = 1
        with pytest.raises(ValidationError):
            section.last_page = 'test'

    def test_topics(self):
        section = pdf.Section(**{'FirstPage': 1, 'LastPage': 1})
        assert section.topics == pdf.UNCHECKED
        v = ['Navigation', 'Trigonometry']
        section.topics = v
        assert section.topics == v
        section.topics = []
        assert section.topics == []
        section.topics = pdf.UNCHECKED
        assert section.topics == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.topics = 'test'


class TestReadWrite:
    def test_all_unchecked(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            book.title = pdf.UNCHECKED
            book.write()

    def test_all_unchecked_structs(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            book.sections = [pdf.Section(**{'FirstPage': 1, 'LastPage': 2})]
            book.plates = pdf.Plate(**{'Page': 3})
            book.signatures = pdf.Signature(**{'Page': 4})

    def test_all_null(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            book.url = book.date_published = book.publishing_frequency = book.title = book.subtitle = book.long_title = book.edition = book.volume = book.in_copyright = book.printing_number = book.numbers_offset = book.roman_numbers_offset = book.has_ligatures = None
            book.authors = []
            book.editors = []
            book.translators = []
            book.copyright_years = []
            book.publishers = []
            book.publisher_cities = []
            book.printers = []
            book.book_topics = []
            book.blank_pages = []
            book.title_pages = []
            book.publishing_info_pages = []
            book.front_cover_pages = []
            book.back_cover_pages = []
            book.end_paper_pages = []
            book.printing_info_pages = []
            book.half_title_pages = []
            book.frontispiece_pages = []
            book.illustration_pages = []
            book.advertisement_partial_pages = []
            book.advertisement_full_pages = []
            book.photograph_pages = []
            book.sections = []
            book.plates = []
            book.signatures = []
            book.write()

    def test_all_null_struct(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            book.url = book.date_published = book.publishing_frequency = book.title = book.subtitle = book.long_title = book.edition = book.volume = book.in_copyright = book.printing_number = book.numbers_offset = book.roman_numbers_offset = None
            book.authors = []
            book.editors = []
            book.translators = []
            book.copyright_years = []
            book.publishers = []
            book.publisher_cities = []
            book.printers = []
            book.book_topics = []
            book.blank_pages = []
            book.title_pages = []
            book.publishing_info_pages = []
            book.front_cover_pages = []
            book.back_cover_pages = []
            book.end_paper_pages = []
            book.printing_info_pages = []
            book.half_title_pages = []
            book.frontispiece_pages = []
            book.illustration_pages = []
            book.advertisement_partial_pages = []
            book.advertisement_full_pages = []
            book.photograph_pages = []
            book.sections = pdf.Section()
            book.plates = pdf.Plate()
            book.signatures = pdf.Signature()
            book.write()

    def test_all_values(self):
        pass