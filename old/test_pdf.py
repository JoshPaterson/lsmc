import old.pdf as pdf
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
            book.url = ''
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
        with pytest.raises(ValidationError):
            book.authors = ['']

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
        with pytest.raises(ValidationError):
            book.editors = ['']

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
        with pytest.raises(ValidationError):
            book.translators = ['']

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
        with pytest.raises(ValidationError):
            book.date_published = ''

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
        with pytest.raises(ValidationError):
            book.publishing_frequency = ''

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
        with pytest.raises(ValidationError):
            book.title = ''

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
        with pytest.raises(ValidationError):
            book.subtitle = ''

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
        with pytest.raises(ValidationError):
            book.long_title = ''

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
        with pytest.raises(ValidationError):
            book.edition = ''

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
        with pytest.raises(ValidationError):
            book.volume = ''

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
        with pytest.raises(ValidationError):
            book.in_copyright = ''

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
        with pytest.raises(ValidationError):
            book.copyright_years = None
        with pytest.raises(ValidationError):
            book.copyright_years = ['']

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
            book.copyright_years = None
        with pytest.raises(ValidationError):
            book.publishers = 'test'
        with pytest.raises(ValidationError):
            book.publishers = ['']

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
            book.publisher_cities = None
        with pytest.raises(ValidationError):
            book.publisher_cities = 'test'
        with pytest.raises(ValidationError):
            book.publisher_cities = ['']

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
            book.printers = None
        with pytest.raises(ValidationError):
            book.printers = 'test'
        with pytest.raises(ValidationError):
            book.printers = ['']

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
        with pytest.raises(ValidationError):
            book.printing_number = ''

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
        with pytest.raises(ValidationError):
            book.numbers_offset = ''
        with pytest.raises(ValidationError):
            book.numbers_offset = 50

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
        with pytest.raises(ValidationError):
            book.roman_numbers_offset = ''
        with pytest.raises(ValidationError):
            book.roman_numbers_offset = 50

    def test_has_ligatures(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 48})
        assert book.has_ligatures == pdf.UNCHECKED
        book.has_ligatures = True
        assert book.has_ligatures == True
        book.has_ligatures = pdf.UNCHECKED
        assert book.has_ligatures == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.has_ligatures = []
        with pytest.raises(ValidationError):
            book.has_ligatures = None
        with pytest.raises(ValidationError):
            book.has_ligatures = ''

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
            book.book_topics = None
        with pytest.raises(ValidationError):
            book.book_topics = 'test'
        with pytest.raises(ValidationError):
            book.book_topics = ['']

    def test_page_tags(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34})
        assert book.page_tags == pdf.UNCHECKED
        book.page_tags = [pdf.PageTag(**{'Kind': 'blank', 'Pages': [1, 3, 5], 'PageCount': book.page_count}), pdf.PageTag(**{'Kind': 'title', 'Pages': [4], 'PageCount': book.page_count})]
        assert book.page_tags[0].kind == 'blank'
        assert book.page_tags[0].pages == [1, 3, 5]
        assert book.page_tags[1].kind == 'title'
        assert book.page_tags[1].pages == [4]
        with pytest.raises(ValidationError):
            book.page_tags[0].pages = ['']
        book.page_tags = []
        assert book.page_tags == []
        book.page_tags = pdf.UNCHECKED
        assert book.page_tags == pdf.UNCHECKED


    def test_sections(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34})
        book.sections = [pdf.Section(**{'HeadingPage': 1, 'PageCount': book.page_count}),
                         pdf.Section(**{'HeadingPage': 6, 'PageCount': book.page_count})]
        assert book.sections[0].heading_page == 1
        assert book.sections[1].heading_page == 6
        with pytest.raises(ValidationError):
            book.sections[0].heading_page = 40
        with pytest.raises(ValidationError):
            book.sections[0].first_page = 40
        with pytest.raises(ValidationError):
            book.sections[0].last_page = 40
        book.sections = []
        assert book.sections == []
        book.sections = pdf.UNCHECKED
        assert book.sections == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            book.sections = None
        with pytest.raises(ValidationError):
            book.sections = 'test'
        with pytest.raises(ValidationError):
            book.sections = ['']
        with pytest.raises(ValidationError):
            book.sections = [[]]
        with pytest.raises(ValidationError):
            book.sections = ([],)

    def test_graphics(self):
        book = pdf.Pdf(**{'SourceFile': 'test/test.pdf', 'PageCount': 34})
        book.graphics = [pdf.Graphic(**{'FirstPage': 2, 'PageCount': book.page_count}),
                       pdf.Graphic(**{'FirstPage': 3, 'PageCount': book.page_count})]
        assert book.graphics[0].first_page == 2
        assert book.graphics[1].first_page == 3
        with pytest.raises(ValidationError):
            book.graphics[0].first_page = 40
        book.graphics = pdf.UNCHECKED
        assert book.graphics == pdf.UNCHECKED
        book.graphics = []
        assert book.graphics == []
        with pytest.raises(ValidationError):
            book.graphics = None
        with pytest.raises(ValidationError):
            book.graphics = 'test'
        with pytest.raises(ValidationError):
            book.graphics = ['']


class TestPageTagFields:
    def test_kind(self):
        page_tag = pdf.PageTag(**{'Kind': 'blank', 'PageCount': 34})
        assert page_tag.kind == 'blank'
        v = 'title'
        page_tag.kind= v
        assert page_tag.kind == v
        with pytest.raises(ValidationError):
            page_tag.kind = None
        with pytest.raises(ValidationError):
            page_tag.kind = []
        with pytest.raises(ValidationError):
            page_tag.kind = ''

    def test_pages(self):
        page_tag = pdf.PageTag(**{'Kind': 'blank', 'PageCount': 34})
        assert page_tag.pages == []
        v = [1, 3, 5]
        page_tag.pages = v
        assert page_tag.pages == v
        page_tag.pages = []
        assert page_tag.pages == []
        with pytest.raises(ValidationError):
            page_tag.pages = None
        with pytest.raises(ValidationError):
            page_tag.pages = ''
        with pytest.raises(ValidationError):
            page_tag.pages = 3

class TestGraphicFields:
    def test_kind(self):
        graphic = pdf.Graphic(**{'FirstPage': 2, 'PageCount': 4})
        assert graphic.kind == pdf.UNCHECKED
        v = 'engraving'
        graphic.kind = v
        assert graphic.kind == v
        graphic.kind = None
        assert graphic.kind == None
        graphic.kind = pdf.UNCHECKED
        assert graphic.kind == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            graphic.kind = []
        with pytest.raises(ValidationError):
            graphic.kind = ''

    def test_content(self):
        graphic = pdf.Graphic(**{'FirstPage': 2, 'PageCount': 4})
        assert graphic.content == pdf.UNCHECKED
        v = 'engraving'
        graphic.content = v
        assert graphic.content == v
        graphic.content = None
        assert graphic.content == None
        graphic.content = pdf.UNCHECKED
        assert graphic.content == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            graphic.content = []
        with pytest.raises(ValidationError):
            graphic.content = ''

    def test_first_page(self):
        graphic = pdf.Graphic(**{'FirstPage': 2, 'PageCount': 4})
        assert graphic.first_page == 2
        v = 3
        graphic.first_page = v
        assert graphic.first_page == v
        with pytest.raises(ValidationError):
            graphic.first_page = pdf.UNCHECKED
        with pytest.raises(ValidationError):
            graphic.first_page = None
        with pytest.raises(ValidationError):
            graphic.first_page = []
        with pytest.raises(ValidationError):
            graphic.first_page = ''

    def test_last_page(self):
        graphic = pdf.Graphic(**{'FirstPage': 2, 'PageCount': 4})
        assert graphic.last_page == pdf.UNCHECKED
        v = 3
        graphic.last_page = v
        assert graphic.last_page == v
        graphic.last_page = pdf.UNCHECKED
        assert graphic.last_page == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            graphic.last_page = 1
        with pytest.raises(ValidationError):
            graphic.last_page = 7
        with pytest.raises(ValidationError):
            graphic.last_page = None
        with pytest.raises(ValidationError):
            graphic.last_page = []
        with pytest.raises(ValidationError):
            graphic.last_page = ''


class TestSectionFields:
    def test_kind(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
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
        with pytest.raises(ValidationError):
            section.kind = []
        with pytest.raises(ValidationError):
            section.kind = ''

    def test_kind_in_book(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
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
        with pytest.raises(ValidationError):
            section.kind_in_book = ''

    def test_title(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
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
        with pytest.raises(ValidationError):
            section.title = ''

    def test_authors(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
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
        with pytest.raises(ValidationError):
            section.authors = ['']

    def test_number(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
        assert section.number == pdf.UNCHECKED
        v = 4
        section.number = v
        assert section.number == v
        section.number = None
        assert section.number == None
        section.number = pdf.UNCHECKED
        assert section.number == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.number = []
        with pytest.raises(ValidationError):
            section.number = ''

    def test_number_kind(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
        assert section.number_kind == pdf.UNCHECKED
        v = 'arabic'
        section.number_kind = v
        assert section.number_kind == v
        section.number_kind = None
        assert section.number_kind == None
        section.number_kind = pdf.UNCHECKED
        assert section.number_kind == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.number_kind = ''
        with pytest.raises(ValidationError):
            section.number_kind = []

    def test_for_edition(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
        assert section.for_edition == pdf.UNCHECKED
        v = 2
        section.for_edition = v
        assert section.for_edition == v
        section.for_edition = None
        assert section.for_edition == None
        section.for_edition = pdf.UNCHECKED
        assert section.for_edition == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.for_edition = ''
        with pytest.raises(ValidationError):
            section.for_edition = []

    def test_heading_page(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
        v = 2
        section.heading_page = v
        assert section.heading_page == v
        with pytest.raises(ValidationError):
            section.heading_page = pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.heading_page = None
        with pytest.raises(ValidationError):
            section.heading_page = ''
        with pytest.raises(ValidationError):
            section.heading_page = []
        with pytest.raises(ValidationError):
            section.heading_page = 30

    def test_first_page(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
        assert section.first_page == pdf.UNCHECKED
        v = 1
        section.first_page = v
        assert section.first_page == v
        section.first_page = pdf.UNCHECKED
        assert section.first_page == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.first_page = None
        with pytest.raises(ValidationError):
            section.first_page = 4
        with pytest.raises(ValidationError):
            section.first_page = ''
        with pytest.raises(ValidationError):
            section.first_page = []

    def test_last_page(self):
        section = pdf.Section(**{'HeadingPage': 2, 'PageCount': 20})
        assert section.last_page == pdf.UNCHECKED
        v = 2
        section.last_page = v
        assert section.last_page == v
        section.last_page = pdf.UNCHECKED
        assert section.last_page == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.last_page = None
        with pytest.raises(ValidationError):
            section.last_page = 1
        with pytest.raises(ValidationError):
            section.last_page = ''
        with pytest.raises(ValidationError):
            section.last_page = []

    def test_section_topics(self):
        section = pdf.Section(**{'HeadingPage': 1, 'PageCount': 20})
        assert section.section_topics == pdf.UNCHECKED
        v = ['Navigation', 'Trigonometry']
        section.section_topics = v
        assert section.section_topics == v
        section.section_topics = []
        assert section.section_topics == []
        section.section_topics = pdf.UNCHECKED
        assert section.section_topics == pdf.UNCHECKED
        with pytest.raises(ValidationError):
            section.section_topics = None
        with pytest.raises(ValidationError):
            section.section_topics = 'test'
        with pytest.raises(ValidationError):
            section.section_topics = ['']


class TestReadWrite:
    def test_all_unchecked(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            book.write()

    def test_all_unchecked_structs(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            book.sections = [pdf.Section(**{'HeadingPage': 3, 'PageCount': 34})]
            book.graphics = [pdf.Plate(**{'FirstPage': 3, 'PageCount': 34})]
            book.page_tags = [pdf.PageTag(**{'kind': 'blank', 'PageCount': 34})]
            book.write()

    def test_all_null(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            for field in pdf.str_fields:
                book[field] = None
            for field in pdf.bool_fields:
                book[field] = None
            for field in pdf.int_fields:
                book[field] = None
            for field in pdf.list_fields:
                book[field] = []
            for field in pdf.struct_fields:
                book[field] = []
            book.write()

    def test_all_null_struct(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            for field in pdf.str_fields:
                book[field] = None
            for field in pdf.bool_fields:
                book[field] = None
            for field in pdf.int_fields:
                book[field] = None
            for field in pdf.list_fields:
                book[field] = []

            book.sections = [pdf.Section(**{'HeadingPage': 3, 'PageCount': 34})]
            for field in pdf.section_str_fields:
                book.sections[0][field] = None
            for field in pdf.section_int_fields.remove('heading_page'):
                book.sections[0][field] = None
            for field in pdf.section_list_fields:
                book.sections[0][field] = []

            book.graphics = [pdf.Plate(**{'FirstPage': 3, 'PageCount': 34})]
            for field in pdf.graphic_str_fields:
                book.graphics[0][field] = None
            for field in pdf.graphic_int_fields.remove('first_page'):
                book.graphics[0][field] = None
            for field in pdf.graphic_list_fields:
                book.graphics[0][field] = []

            book.page_tags = [pdf.PageTag(**{'kind': 'blank', 'PageCount': 34})]
            book.page_tags[0].pages = []

            book.write()

    def test_all_values(self):
        with temp_copy('empty_no_metadata.pdf') as pdf_path:
            book = pdf.Pdf.from_path(pdf_path)
            book.url = 'testing.org/testing'
            book.authors = ['testing', 'testing2']
            book.editors = ['testing', 'testing2']
            book.translators = ['testing', 'testing2']
            book.date_published = '1763-03-14'
            book.publishing_frequency = 'monthly'
            book.title = 'testing'
            book.subtitle = 'testing'
            book.long_title = 'testingtesting'
            book.edition = 1
            book.volume = 1
            book.in_copyright = False
            book.publishers = ['testing', 'testing']
            book.publisher_cities = ['testing', 'testing']
            book.printers = ['testing', 'testing']
            book.printing_number = 1
            book.numbers_offset = 2
            book.roman_numbers_offset = 3
            book.has_ligatures = True
            book.book_topics = ['testing', 'testing']

            book.sections = [pdf.Section(**{'HeadingPage': 3, 'PageCount': 34})]
            book.sections[0].kind = 'chapter'
            book.sections[0].kind_in_book = 'chapter'
            book.sections[0].title = 'Trigonometry'
            book.sections[0].authors = ['testing', 'testing']
            book.sections[0].number = 2
            book.sections[0].number_kind = 'arabic'
            book.sections[0].for_edition = 2
            book.sections[0].first_page = 2
            book.sections[0].last_page = 4
            book.sections[0].section_topics = ['testing', 'testing']

            book.graphics = [pdf.Plate(**{'FirstPage': 3, 'PageCount': 34})]
            book.graphics[0].kind = 'plate'
            book.graphics[0].content = 'map'
            book.graphics[0].last_page = 4
            book.graphics[0].color = 'grayscale'

            book.page_tags = [pdf.PageTag(**{'kind': 'blank', 'PageCount': 34})]
            book.page_tags[0].pages = [2, 3, 4]

            book.write()