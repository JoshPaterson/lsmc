from hashlib import blake2b
from django.db import models
from treenode.models import TreeNodeModel
from django.utils.html import mark_safe

class City(models.Model):
    name = models.CharField(max_length=31)
    # books (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class Topic(TreeNodeModel):
    name = models.CharField(max_length=31)
    treenode_display_field = 'name'
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children')
    # books (MtM)
    # sections (MtM)
    # pages (MtM)
    # children (OtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Creator(models.Model):
    # books (MtM)
    # sections (MtM)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    # books (MtM)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Printer(models.Model):
    # books (MtM)
    name = models.CharField(max_length=63)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CopyrightYear(models.Model):
    year = models.IntegerField()
    # books (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.year


class Page(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='pages')
    number = models.PositiveIntegerField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)
    image = models.ImageField(upload_to='pages')
    graphics = models.ManyToManyField('Graphic', blank=True)
    # sections (MtM)
    # section_headings (OtM)
    # kinds (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.book)}: pg.{self.number}'

    def image_tag(self):
        return mark_safe(f'<img src="/{self.image}" />')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    class Meta:
        ordering = ['number']


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
        APPENDICES = 'APS'
        APPENDIX = 'APP'
        INDEX = 'IND'
        PUBLISHERS_CATALOG = 'CAT'
        TABLE = 'TAB'
        TABLES = 'TAS'
        ARTICLE = 'ART'
        FIGURE = 'FIG'
        PLATES = 'PLA'

    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='sections')
    kind = models.CharField(max_length=3, choices=Kind.choices, blank=True)
    kind_checked = models.BooleanField(default=False, blank=True)
    kind_in_book = models.CharField(max_length=15, blank=True)
    kind_in_book_checked = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=100, blank=True)
    title_checked = models.BooleanField(default=False, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    number_checked = models.BooleanField(default=False, blank=True)
    number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    number_kind_checked = models.BooleanField(default=False, blank=True)
    caption = models.TextField(blank=True)
    caption_checked = models.BooleanField(default=False, blank=True)
    for_edition = models.PositiveIntegerField(null=True, blank=True)
    for_edition_checked = models.BooleanField(default=False, blank=True)
    heading_page = models.ForeignKey(Page, on_delete=models.RESTRICT, related_name='section_headings')
    pages = models.ManyToManyField(Page, blank=True)
    pages_checked = models.BooleanField(default=False, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)
    topics_checked = models.BooleanField(default=False, blank=True)
    authors = models.ManyToManyField(Creator, related_name='authored_sections', blank=True)
    editors = models.ManyToManyField(Creator, related_name='edited_sections', blank=True)
    translators = models.ManyToManyField(Creator, related_name='translated_sections', blank=True)
    creators_checked = models.BooleanField(default=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.book)} {self.kind.capitalize()} {self.number}'

    class Meta:
        ordering = ['heading_page']


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

    document_id = models.UUIDField(max_length=50, null=True, blank=True)
    url = models.URLField(blank=True)
    downloaded_at = models.DateField(null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)
    date_published_checked = models.BooleanField(default=False, blank=True)
    publishing_frequency = models.CharField(max_length=1, choices=PublishingFrequency.choices, blank=True)
    publishing_frequency_checked = models.BooleanField(default=False, blank=True)
    scan_color = models.CharField(max_length=3, choices=Color.choices, blank=True)
    scan_color_checked = models.BooleanField(default=False, blank=True)
    title = models.CharField(max_length=100, blank=True)
    title_checked = models.BooleanField(default=False, blank=True)
    subtitle = models.CharField(max_length=100, blank=True)
    subtitle_checked = models.BooleanField(default=False, blank=True)
    edition_number = models.PositiveIntegerField(null=True, blank=True)
    edition_number_checked = models.BooleanField(default=False, blank=True)
    volume_number = models.PositiveIntegerField(null=True, blank=True)
    volume_number_checked = models.BooleanField(default=False, blank=True)
    volume_number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    volume_number_kind_checked = models.BooleanField(default=False, blank=True)
    printing_number = models.PositiveIntegerField(null=True, blank=True)
    printing_number_checked = models.BooleanField(default=False, blank=True)
    numbers_offset = models.PositiveIntegerField(null=True, blank=True)
    numbers_offset_checked = models.BooleanField(default=False, blank=True)
    roman_numbers_offset = models.PositiveIntegerField(null=True, blank=True)
    roman_numbers_offset_checked = models.BooleanField(default=False, blank=True)
    in_copyright = models.BooleanField(null=True, blank=True)
    in_copyright_checked = models.BooleanField(default=False, blank=True)
    has_ligatures = models.BooleanField(null=True, blank=True)
    has_ligatures_checked = models.BooleanField(default=False, blank=True)
    cities = models.ManyToManyField(City, blank=True)
    cities_checked = models.BooleanField(default=False, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)
    topics_checked = models.BooleanField(default=False, blank=True)
    authors = models.ManyToManyField(Creator, related_name='authored_books', blank=True)
    editors = models.ManyToManyField(Creator, related_name='edited_books', blank=True)
    translators = models.ManyToManyField(Creator, related_name='translated_books', blank=True)
    creators_checked = models.BooleanField(default=False, blank=True)
    printers = models.ManyToManyField(Printer, blank=True)
    printers_checked = models.BooleanField(default=False, blank=True)
    publishers = models.ManyToManyField(Publisher, blank=True)
    publishers_checked = models.BooleanField(default=False, blank=True)
    copyright_years = models.ManyToManyField(CopyrightYear, blank=True)
    copyright_years_checked = models.BooleanField(default=False, blank=True)
    # pages (OtM)
    # sections (OtM)
    sections_checked = models.BooleanField(default=False, blank=True)
    # graphics (OtM)
    graphics_checked = models.BooleanField(default=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        string = f'{self.date_published.year}: {self.title}'
        if self.volume_number:
            string += f' Vol. {self.volume_number}'
        return string

    class Meta:
        pass


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
        FULL_AD = 'FAD'
        PARTIAL_AD = 'PAD'
        EQUATIONS = 'EQS'
        GRAPHICS = 'GRA'

    pages = models.ManyToManyField(Page, blank=True)
    name = models.CharField(max_length=3, choices=Kind.choices)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


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
        DRAWING = 'DRA'
        DECORATION = 'DEC'

    class Color(models.TextChoices):
        COLOR = 'COL'
        BITONAL = 'BIT'
        GRAYSCALE = 'GRA'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='graphics')
    medium = models.CharField(max_length=3, choices=Medium.choices, blank=True)
    medium_checked = models.BooleanField(default=False, blank=True)
    content = models.CharField(max_length=3, choices=Content.choices, blank=True)
    content_checked = models.BooleanField(default=False, blank=True)
    print_color = models.CharField(max_length=3, choices=Color.choices, blank=True)
    print_color_checked = models.BooleanField(default=False, blank=True)
    # pages (MtM)
    pages_checked = models.BooleanField(default=False, blank=True)
    artists = models.ManyToManyField(Creator)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.kind} on pg. {self.pages[0].number} of {self.book}'