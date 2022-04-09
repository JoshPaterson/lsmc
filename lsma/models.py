from django.db import models
from django.contrib.auth.models import User
from treenode.models import TreeNodeModel
from django.utils.html import mark_safe
from django.contrib.postgres.fields import ArrayField
from django_extensions.db.models import TimeStampedModel
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail


class NumberKind(models.TextChoices):
    ARABIC = '1'
    ROMAN_UPPER = 'I'
    ROMAN_LOWER = 'i'
    LETTER_UPPER = 'A'
    LETTER_LOWER = 'a'


class Topic(TreeNodeModel, TimeStampedModel):
    name = models.CharField(max_length=31, unique=True)
    treenode_display_field = 'name'
    # books (MtM)
    # sections (MtM)
    # pages (MtM)
    # tables (MtM)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/topics/{self.name}'


class Person(TimeStampedModel):
    # books (MtM)
    # sections (MtM)
    family_name = models.CharField(max_length=31)
    given_names = models.CharField(max_length=31, blank=True)

    class Meta:
        unique_together = ['family_name', 'given_names']

    def get_full_name(self):
        name = self.family_name
        if self.given_names:
            name = name + f', {self.given_names}'
        return name

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return f'/persons/{self.get_full_name()}'


class Contribution(models.Model):
    class Role(models.TextChoices):
        AUTHOR = 'AUT'
        EDITOR = 'EDI'
        TRANSLATOR = 'TRA'
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='contributions')
    kind = models.CharField(max_length=3, choices=Role.choices)
    rank = models.PositiveSmallIntegerField()


class Page(TimeStampedModel):
    class ImageProblem(models.TextChoices):
        DARK_BACKGROUND = 'DBA'
        ROTATION = 'ROT'
        DOUBLE_PAGE = 'DOU'
        WATERMARK = 'WAT'

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

    class Direction(models.TextChoices):
        LEFT = 'L'
        RIGHT = 'R'

    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='pages')
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)
    original_image = models.ImageField(unique=True)
    thumbnail = ImageSpecField(source='original_image',
                               processors=[Thumbnail(height=200)],
                               format='JPEG',
                               options={'quality': 60})
    jpg_image = ImageSpecField(source='original_image',
                                format='JPEG',
                                options={'quality': 80})
    graphics = models.ManyToManyField('graphic', blank=True)
    text = models.TextField(blank=True, null=True)
    text_generated_at = models.DateTimeField(blank=True, null=True)
    # sections (MtM)
    # section_headings (OtM)
    # tables (MtM)
    kinds = ArrayField(models.CharField(max_length=3, choices=Kind.choices), null=True, blank=True)
    image_problems = ArrayField(models.CharField(max_length=3, choices=ImageProblem.choices), null=True, blank=True)
    text_top_rotated_to = models.CharField(max_length=1, blank=True, null=True, choices=Direction.choices)

    def __str__(self):
        return f'pg. {self.number}'

    def image_tag(self):
        return mark_safe(f'<img src="{self.jpg_image.url}" width="800"/>')

    def thumbnail_tag(self):
        return mark_safe(f'<img src="{self.thumbnail.url}" />')

    class Meta:
        ordering = ['number']

    def get_absolute_url(self):
        return f'{self.book.get_absolute_url()}/page/{self.number}'


class Section(TimeStampedModel):
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
    for_edition = models.PositiveSmallIntegerField(null=True, blank=True)
    for_edition_checked = models.DateTimeField(blank=True, null=True)
    heading_page = models.ForeignKey(Page, on_delete=models.RESTRICT, related_name='section_headings')
    pages = models.ManyToManyField(Page, blank=True)
    first_page_checked = models.DateTimeField(blank=True, null=True)
    last_page_checked = models.DateTimeField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)
    topics_checked = models.DateTimeField(blank=True, null=True)
    contributions = models.ManyToManyField(Contribution, blank=True)
    contributions_checked = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{str(self.book)} {self.kind.capitalize()} {self.number}'

    def get_absolute_url(self):
        if self.kind & self.number:
            return f'{self.book.get_absolute_url()}/{self.kind}/{self.number}'
        else:
            return f'{self.book.get_absolute_url()}/section/{self.id}'

    class Meta:
        ordering = ['heading_page']


class Book(TimeStampedModel):
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
    subtitle = models.TextField(blank=True)
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
    cities = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    cities_checked = models.DateTimeField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True)
    topics_checked = models.DateTimeField(blank=True, null=True)
    contributions = models.ManyToManyField(Contribution, blank=True)
    contributions_checked = models.DateTimeField(blank=True, null=True)
    printers = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    printers_checked = models.DateTimeField(blank=True, null=True)
    publishers = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    publishers_checked = models.DateTimeField(blank=True, null=True)
    copyright_years = ArrayField(models.PositiveSmallIntegerField(), blank=True, null=True)
    copyright_years_checked = models.DateTimeField(blank=True, null=True)
    # pages (OtM)
    # sections (OtM)
    sections_checked = models.DateTimeField(blank=True, null=True)
    # graphics (OtM)
    graphics_checked = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    hidden = models.BooleanField(blank=True, default=False)
    other_languages = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    other_languages_checked = models.DateTimeField(blank=True, null=True)
    series_name = models.CharField(max_length=63, blank=True, null=True)
    number_in_series = models.PositiveSmallIntegerField(blank=True, null=True)
    number_in_series_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    series_checked = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if full_title := self.get_full_title():
            return full_title
        else:
            return str(self.uuid)

    def make_slug(self):
        slug = str(self.date_published.year)
        if person:=self.contributions[0].family_name:
            slug = slug + f'-{person}'
        if self.title:
            slug = slug + f'-{self.title}'
        return slug

    def get_full_title(self):
        full_title = ''
        if self.title:
            title = full_title + self.title
        if self.volume_number:
            full_title = full_title + f' vol. {self.volume_number}'
        if self.edition_number:
            full_title = full_title + f' ed. {self.edition_number}'
        if self.issue_number:
            full_title = full_title + f' is. {self.issue_number}'
        return full_title



    def get_absolute_url(self):
        if self.slug:
            return f'books/{self.slug}'
        else:
            return f'books/{self.uuid}'

    class Meta:
        get_latest_by = 'date_published'


class Graphic(TimeStampedModel):
    class Medium(models.TextChoices):
        ENGRAVED_PLATE = 'ENG'
        ETCHING = 'ETC'
        WOODCUT = 'WOO'
        LITHOGRAPH = 'LIT'
        MEZZOTINT = 'MEZ'
        AQUATINT = 'AQU'
        # see art of engraving, with the various modes of operation Under the Following Different Divisions: Eching, Soft-ground Etching, Line-engraving, Dhalk and Stipple, Aquiatint, Mezzotint, Lithography, Wood Engraving, Medallic Engraving, Electrography, and Photography: Illustrated with Specimens of the Different Styles of Engraving. London: Ackermann and Co., 1841

    class Content(models.TextChoices):
        PHOTOGRAPH = 'PHO'
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
    artists = models.ManyToManyField(Person)
    caption = models.TextField(blank=True)
    caption_checked = models.DateTimeField(blank=True, null=True)
    left = models.PositiveSmallIntegerField(null=True, blank=True)
    top = models.PositiveSmallIntegerField(null=True, blank=True)
    width = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    caption_left = models.PositiveSmallIntegerField(null=True, blank=True)
    caption_top = models.PositiveSmallIntegerField(null=True, blank=True)
    caption_width = models.PositiveSmallIntegerField(null=True, blank=True)
    caption_height = models.PositiveSmallIntegerField(null=True, blank=True)
    box_checked = models.DateTimeField(blank=True, null=True)
    caption_box_checked = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.kind} on pg. {self.pages[0].number} of {self.book}'

    def get_absolute_url(self):
        return f'{self.book.get_absolute_url()}/graphic/{self.id}'

class Box(TimeStampedModel):
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

    class Meta:
        verbose_name_plural = 'boxes'

    def __str__(self):
        return f'{self.page_number}:{self.block_number}:{self.paragraph_number}:{self.line_number}:{self.word_number}:{self.text}'

    def image_tag(self):
        return mark_safe(f'<img src="boxes/{str(self.page.book.slug)}/{self.page.number}/{self.level}/{self.page_number}/{self.block_number}/{self.paragraph_number}/{self.line_number}/{self.word_number}" />')

    def get_absolute_url(self):
        if self.level == self.Level.PAGE:
            number = self.page_number
        if self.level == self.Level.BLOCK:
            number = self.block_number
        if self.level == self.Level.PARAGRAPH:
            number = self.paragraph_number
        if self.level == self.Level.LINE:
            number = self.line_number
        if self.level == self.Level.WORD:
            number = self.word_number
        return f'{self.page.get_absolute_url()}/{self.level}/{number}'


class Table(TimeStampedModel):
    heading_page = models.ForeignKey(Page, on_delete=models.CASCADE)
    pages = models.ManyToManyField(Page, related_name='tables')
    pages_checked = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=63, blank=True, null=True)
    title_checked = models.DateTimeField(blank=True, null=True)
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    number_checked = models.DateTimeField(blank=True, null=True)
    number_kind = models.CharField(max_length=1, blank=True, choices=NumberKind.choices)
    number_kind_checked = models.DateTimeField(blank=True, null=True)
    inputs = ArrayField(models.CharField(max_length=63), null=True, blank=True)
    inputs_checked = models.DateTimeField(blank=True, null=True)
    outputs = ArrayField(models.CharField(max_length=63), null=True, blank=True)
    outputs_checked = models.DateTimeField(blank=True, null=True)
    topics = models.ManyToManyField(Topic)
    topics_checked = models.DateTimeField(blank=True, null=True)


class OcrFix(TimeStampedModel):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='ocr_fixes')
    user_accuracy = models.FloatField()
    word = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='ocr_fixes')
    old_value = models.CharField(max_length=31, null=True)
    new_value = models.CharField(max_length=31, null=True)
    is_correct = models.BooleanField(blank=True, null=True)
    decided_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'ocr fixes'