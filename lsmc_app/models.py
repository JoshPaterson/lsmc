from django.db import models

class City(models.Model):
    name = models.CharField(max_length=31)
    # books (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'cities'


class Topic(models.Model):
    name = models.CharField(max_length=31)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')
    # books (MtM)
    # sections (MtM)
    # pages (MtM)
    # children (OtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    class NumberKind(models.TextChoices):
        ARABIC = '1'
        ROMAN_UPPER = 'I'
        ROMAN_LOWER = 'i'
        LETTER_UPPER = 'A'
        LETTER_LOWER = 'a'

    class Color(models.TextChoices):
        COLOR = 'COL'
        BITONAL = 'BIT'
        GRAYSCALE = 'GRA'

    class PublishingFrequency(models.TextChoices):
        YEARLY = 'Y'
        QUARTERLY = 'Q'
        MONTHLY = 'M'
        WEEKLY = 'W'
        DAILY = 'D'

    pdf = models.FileField(upload_to='pdf')
    document_id = models.CharField(max_length=50)
    instance_id = models.CharField(max_length=50)
    url = models.URLField()
    date_published = models.DateField()
    date_published_checked = models.BooleanField()
    publishing_frequency = models.CharField(max_length=1, choices=PublishingFrequency.choices)
    publishing_frequency_checked = models.BooleanField()
    scan_color = models.CharField(max_length=3, choices=Color.choices)
    scan_color_checked = models.BooleanField()
    title = models.CharField(max_length=100)
    title_checked = models.BooleanField()
    subtitle = models.CharField(max_length=100)
    subtitle_checked = models.BooleanField()
    long_title = models.TextField()
    long_title_checked = models.BooleanField()
    edition = models.PositiveIntegerField()
    edition_checked = models.BooleanField()
    volume = models.PositiveIntegerField()
    volume_checked = models.BooleanField()
    volume_number_kind = models.PositiveIntegerField()
    volume_number_kind = models.BooleanField()
    printing_number = models.PositiveIntegerField()
    printing_number_checked = models.BooleanField()
    numbers_offset = models.PositiveIntegerField()
    numbers_offset_checked = models.BooleanField()
    roman_numbers_offset = models.PositiveIntegerField()
    roman_numbers_offset_checked = models.BooleanField()
    in_copyright = models.BooleanField()
    in_copyright_checked = models.BooleanField()
    has_ligatures = models.BooleanField()
    has_ligatures_checked = models.BooleanField()
    cities = models.ManyToManyField(City)
    cities_checked = models.BooleanField()
    topics = models.ManyToManyField(Topic)
    topics_checked = models.BooleanField()
    # authors (MtM)
    authors_checked = models.BooleanField()
    # editors (MtM)
    editors_checked = models.BooleanField()
    # translators (MtM)
    translators_checked = models.BooleanField()
    # printers (MtM)
    printers_checked = models.BooleanField()
    # publishers (MtM)
    publishers_checked = models.BooleanField()
    # copyright_years (MtM)
    copyright_years_checked = models.BooleanField()
    # pages (OtM)
    # sections (OtM)
    sections_checked = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        string = f'{self.date_published.year}: {self.title}'
        if self.volume:
            string += f' Vol. {self.volume}'
        return f'{self.title} Vol. {self.volume}'

    class Meta:
        # ordering = ['date_published',]
        # unique_together = [['','']]
        pass


class CopyrightYear(models.Model):
    year = models.IntegerField()
    books = models.ManyToManyField(Book)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Page(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    page_number = models.PositiveIntegerField()
    topics = models.ManyToManyField(Topic)
    image = models.ImageField(upload_to='pages')
    # graphics (MtM)
    # sections (MtM)
    # section_headings (OtM)
    # kinds (OtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.book)}: pg.{self.page_number}'

    class Meta:
        ordering = ['page_number']


class Section(models.Model):
    class NumberKind(models.TextChoices):
        ARABIC = '1'
        ROMAN_UPPER = 'I'
        ROMAN_LOWER = 'i'
        LETTER_UPPER = 'A'
        LETTER_LOWER = 'a'

    class Kind(models.TextChoices):
        CHAPTER = 'CHG'
        CHAPTER_GROUP = 'CHA'
        PREFACE = 'PRE'
        INTRODUCTION = 'INT'
        DEDICATION = 'DED'
        ACKNOWLEDGEMENTS = 'ACK'
        TABLE_OF_CONTENTS = 'TOC'
        BIBLIOGRAPHY = 'BIB'
        GLOSSARY = 'GLO'
        APPENDICES = 'APG'
        APPENDIX = 'APP'
        INDEX = 'IND'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='sections')
    kind = models.CharField(max_length=3, choices=Kind.choices)
    kind_checked = models.BooleanField()
    kind_in_book = models.CharField(max_length=15)
    kind_in_book_checked = models.BooleanField()
    title = models.CharField(max_length=100)
    title_checked = models.BooleanField()
    number = models.PositiveIntegerField()
    number_checked = models.BooleanField()
    number_kind = models.CharField(max_length=1, choices=NumberKind.choices)
    number_kind_checked = models.BooleanField()
    for_edition = models.PositiveIntegerField()
    for_edition_checked = models.BooleanField()
    heading_page = models.ForeignKey(Page, on_delete=models.RESTRICT, related_name='section_headings')
    heading_page_checked = models.BooleanField()
    pages = models.ManyToManyField(Page)
    pagesunchecked = models.BooleanField()
    topics = models.ManyToManyField(Topic)
    topics_checked = models.BooleanField()
    # authors (MtM)
    # editors (MtM)
    # translators (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.book)} {self.kind.capitalize()} {self.number}'

    class Meta:
        ordering = ['heading_page']


class Author(models.Model):
    books = models.ManyToManyField(Book)
    sections = models.ManyToManyField(Section)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Editor(models.Model):
    books = models.ManyToManyField(Book)
    sections = models.ManyToManyField(Section)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Translator(models.Model):
    books = models.ManyToManyField(Book)
    sections = models.ManyToManyField(Section)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Publisher(models.Model):
    books = models.ManyToManyField(Book)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Printer(models.Model):
    books = models.ManyToManyField(Book)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PageKind(models.Model):
    class Kind(models.TextChoices):
        BLANK = 'BLA'
        TITLE = 'TIT'
        PUBLISHING_INFO = 'PUB'
        PRINTING_INFO = 'PRI'
        HALF_TITLE = 'HAT'
        FRONT_COVER = 'FCO'
        BACK_COVER = 'BCO'
        FRONT_JACKET = 'FJA'
        BACK_JACKET = 'BJA'
        FRONT_JACKET_FLAP = 'FJF'
        BACK_JACKET_FLAP = 'BJF'
        DECORATIVE_PAPER = 'DEC'

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='kinds')
    name = models.CharField(max_length=3, choices=Kind.choices)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Graphic(models.Model):
    class Medium(models.TextChoices):
        PHOTOGRAPH = 'PHO'
        ENGRAVING = 'ENG'
        LITHOGRAPH = 'LIT'

    class Content(models.TextChoices):
        MAP = 'MAP'
        CHART = 'CHA'
        DIAGRAM = 'DIA'
        ILLUSTRATION = 'ILL'
        TECHNICAL_DRAWING = 'TEC'

    class Color(models.TextChoices):
        COLOR = 'COL'
        BITONAL = 'BIT'
        GRAYSCALE = 'GRA'

    medium = models.CharField(max_length=3, choices=Medium.choices)
    medium_checked = models.BooleanField()
    content = models.CharField(max_length=3, choices=Content.choices)
    content_checked = models.BooleanField()
    print_color = models.CharField(max_length=3, choices=Color.choices)
    print_color_checked = models.BooleanField()
    pages = models.ManyToManyField(Page)
    pages_checked = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
# Create your models here.
