from hashlib import blake2b
from django.db import models
from treenode.models import TreeNodeModel
from django.utils.html import mark_safe

class City(models.Model):
    name = models.CharField(max_length=31, unique=True)
    # books (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/cities/{self.name}'



class Topic(TreeNodeModel):
    name = models.CharField(max_length=31, unique=True)
    treenode_display_field = 'name'
    # books (MtM)
    # sections (MtM)
    # pages (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/topics/{self.name}'


class Creator(models.Model):
    # books (MtM)
    # sections (MtM)
    last_name = models.CharField(max_length=31)
    given_names = models.CharField(max_length=31, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        name = self.last_name
        if self.given_names:
            name = name + f', {self.given_names}'
        return name

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return f'/creators/{self.get_full_name()}'


class Publisher(models.Model):
    # books (MtM)
    name = models.CharField(max_length=63, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/publishers/{self.name}'


class Printer(models.Model):
    # books (MtM)
    name = models.CharField(max_length=63, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/printers/{self.name}'


class CopyrightYear(models.Model):
    year = models.IntegerField(unique=True)
    # books (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.year)

    def get_absolute_url(self):
        return f'/copyright-years/{self.name}'


class Page(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='pages')
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)
    image = models.ImageField(upload_to='pages', unique=True)
    graphics = models.ManyToManyField('Graphic', blank=True)
    text = models.TextField(blank=True)
    # sections (MtM)
    # section_headings (OtM)
    # kinds (MtM)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'pg. {self.number}'

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" />')
    image_tag.short_description = 'Image'

    class Meta:
        ordering = ['number']

    def get_absolute_url(self):
        return f'{self.book.get_absolute_url()}/page/{self.number}'


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
    kind_checked = models.DateTimeField(blank=True, null=True)
    kind_in_book = models.CharField(max_length=15, blank=True)
    kind_in_book_checked = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    title_checked = models.DateTimeField(blank=True, null=True)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    number_checked = models.DateTimeField(blank=True, null=True)
    number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    number_kind_checked = models.DateTimeField(blank=True, null=True)
    caption = models.TextField(blank=True)
    caption_checked = models.DateTimeField(blank=True, null=True)
    for_edition = models.PositiveSmallIntegerField(null=True, blank=True)
    for_edition_checked = models.DateTimeField(blank=True, null=True)
    heading_page = models.ForeignKey(Page, on_delete=models.RESTRICT, related_name='section_headings')
    pages = models.ManyToManyField(Page, blank=True)
    first_page_checked = models.DateTimeField(blank=True, null=True)
    last_page_checked = models.DateTimeField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)
    topics_checked = models.DateTimeField(blank=True, null=True)
    authors = models.ManyToManyField(Creator, related_name='authored_sections', blank=True)
    editors = models.ManyToManyField(Creator, related_name='edited_sections', blank=True)
    translators = models.ManyToManyField(Creator, related_name='translated_sections', blank=True)
    creators_checked = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.book)} {self.kind.capitalize()} {self.number}'

    def get_absolute_url(self):
        if self.kind & self.number:
            return f'{self.book.get_absolute_url()}/{self.kind}/{self.number}'
        else:
            return f'{self.book.get_absolute_url()}/section/{self.id}'

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
        ONCE = 'O'
        YEARLY = 'Y'
        QUARTERLY = 'Q'
        MONTHLY = 'M'
        WEEKLY = 'W'
        DAILY = 'D'

    uuid = models.UUIDField(max_length=36, null=True, blank=True, unique=True)
    url = models.URLField(blank=True, null=True)
    downloaded_at = models.DateField(null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)
    date_published_checked = models.DateTimeField(blank=True, null=True)
    publishing_frequency = models.CharField(max_length=1, choices=PublishingFrequency.choices, blank=True)
    publishing_frequency_checked = models.DateTimeField(blank=True, null=True)
    scan_color = models.CharField(max_length=3, choices=Color.choices, blank=True)
    scan_color_checked = models.DateTimeField(blank=True, null=True)
    title_page = models.OneToOneField(Page, related_name='title_page_for', on_delete=models.SET_NULL, blank=True, null=True)
    title_page_checked = models.DateTimeField(blank=True, null=True)
    copyright_page = models.OneToOneField(Page, related_name='copyright_page_for', on_delete=models.SET_NULL, blank=True, null=True)
    copyright_page_checked = models.DateTimeField(blank=True, null=True)
    has_vector_text = models.BooleanField(null=True)
    has_vector_text_checked = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True)
    title_checked = models.DateTimeField(blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True)
    subtitle_checked = models.DateTimeField(blank=True, null=True)
    edition_number = models.PositiveSmallIntegerField(null=True, blank=True)
    edition_number_checked = models.DateTimeField(blank=True, null=True)
    volume_number = models.PositiveSmallIntegerField(null=True, blank=True)
    volume_number_checked = models.DateTimeField(blank=True, null=True)
    volume_number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    volume_number_kind_checked = models.DateTimeField(blank=True, null=True)
    issue_number = models.PositiveSmallIntegerField(null=True, blank=True)
    issue_number_checked = models.DateTimeField(blank=True, null=True)
    issue_number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    issue_number_kind_checked = models.DateTimeField(blank=True, null=True)
    printing_number = models.PositiveSmallIntegerField(null=True, blank=True)
    printing_number_checked = models.DateTimeField(blank=True, null=True)
    numbers_offset = models.PositiveSmallIntegerField(null=True, blank=True)
    numbers_offset_checked = models.DateTimeField(blank=True, null=True)
    roman_numbers_offset = models.PositiveSmallIntegerField(null=True, blank=True)
    roman_numbers_offset_checked = models.DateTimeField(blank=True, null=True)
    in_copyright = models.BooleanField(null=True, blank=True)
    in_copyright_checked = models.DateTimeField(blank=True, null=True)
    has_ligatures = models.BooleanField(null=True, blank=True)
    has_ligatures_checked = models.DateTimeField(blank=True, null=True)
    cities = models.ManyToManyField(City, blank=True)
    cities_checked = models.DateTimeField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)
    topics_checked = models.DateTimeField(blank=True, null=True)
    authors = models.ManyToManyField(Creator, related_name='authored_books', blank=True)
    editors = models.ManyToManyField(Creator, related_name='edited_books', blank=True)
    translators = models.ManyToManyField(Creator, related_name='translated_books', blank=True)
    creators_checked = models.DateTimeField(blank=True, null=True)
    printers = models.ManyToManyField(Printer, blank=True)
    printers_checked = models.DateTimeField(blank=True, null=True)
    publishers = models.ManyToManyField(Publisher, blank=True)
    publishers_checked = models.DateTimeField(blank=True, null=True)
    copyright_years = models.ManyToManyField(CopyrightYear, blank=True)
    copyright_years_checked = models.DateTimeField(blank=True, null=True)
    # pages (OtM)
    # sections (OtM)
    sections_checked = models.DateTimeField(blank=True, null=True)
    # graphics (OtM)
    graphics_checked = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # string = f'{self.date_published.year}: {self.title}'
        # if self.volume_number:
            # string += f' Vol. {self.volume_number}'
        return str(self.uuid)

    def get_first_creator(self):
        creators = [a.last_name for a in self.authors] + [e.last_name for e in self.editors] + [t.last_name for t in self.translators] + ''
        return creators[0]

    def make_slug(self):
        slug = str(self.date_published.year)
        if creator:=self.get_first_creator():
            slug = slug + f'-{creator}'
        if self.title:
            slug = slug + f'-{self.title}'
        return slug

    def get_absolute_url(self):
        if self.slug:
            return f'books/{self.slug}'
        else:
            return f'books/{self.uuid}'

    class Meta:
        get_latest_by = 'date_published'


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
    name = models.CharField(max_length=3, choices=Kind.choices, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'page-kind/{self.name}'


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
        EQUATION = 'EQU'
        MUSIC_NOTATION = 'MUS'

    class Color(models.TextChoices):
        COLOR = 'COL'
        BITONAL = 'BIT'
        GRAYSCALE = 'GRA'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='graphics')
    medium = models.CharField(max_length=3, choices=Medium.choices, blank=True)
    medium_checked = models.DateTimeField(blank=True, null=True)
    content = models.CharField(max_length=3, choices=Content.choices, blank=True)
    content_checked = models.DateTimeField(blank=True, null=True)
    print_color = models.CharField(max_length=3, choices=Color.choices, blank=True)
    print_color_checked = models.DateTimeField(blank=True, null=True)
    # pages (MtM)
    pages_checked = models.DateTimeField(blank=True, null=True)
    artists = models.ManyToManyField(Creator)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.kind} on pg. {self.pages[0].number} of {self.book}'

    def get_absolute_url(self):
        return f'{self.book.get_absolute_url()}/graphic/{self.id}'

class Box(models.Model):
    class Level(models.IntegerChoices):
        PAGE = 1
        BLOCK = 2
        PARAGRAPH = 3
        LINE = 4
        WORD = 5
    page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True)
    original_text = models.CharField(max_length=32, blank=True, editable=False)
    text = models.CharField(max_length=32, blank=True)
    level = models.PositiveSmallIntegerField(choices=Level.choices)
    page_number = models.PositiveSmallIntegerField()
    block_number = models.PositiveSmallIntegerField()
    paragraph_number = models.PositiveSmallIntegerField()
    line_number = models.PositiveSmallIntegerField()
    word_number = models.PositiveSmallIntegerField()
    left = models.PositiveSmallIntegerField()
    top = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    original_confidence = models.FloatField(blank=True, null=True, editable=False)
    confidence = models.FloatField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'boxes'

    def __str__(self):
        return f'{self.page_number}:{self.block_number}:{self.paragraph_number}:{self.line_number}:{self.word_number}:{self.text}'

    def get_absolute_url(self):
        return f'box/{self.id}'