from django.db import models
from django.contrib.auth.models import User
from treenode.models import TreeNodeModel
from django.utils.html import mark_safe
from django.contrib.postgres.fields import ArrayField
from django_extensions.db.models import TimeStampedModel
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from .text import word_list_to_text
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class NumberKind(models.TextChoices):
    ARABIC = '1'
    ROMAN_UPPER = 'I'
    ROMAN_LOWER = 'i'
    LETTER_UPPER = 'A'
    LETTER_LOWER = 'a'
    ORDINAL_WORD = 'F'
    ORDINAL_NUMBER = 'f'


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
        verbose_name_plural = 'people'

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
        BOOKPLATE = 'BOO'
        OTHER = 'OTH'

    class Rotation(models.TextChoices):
        CLOCKWISE = 'R'
        COUNTERCLOCKWISE = 'L'
        UPSIDE_DOWN = 'U'

    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='pages')
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    topics = models.ManyToManyField(Topic, blank=True, related_name='pages')
    original_image = models.ImageField(unique=True, width_field='width', height_field='height')
    thumbnail = ImageSpecField(source='original_image',
                               processors=[Thumbnail(height=200)],
                               format='JPEG',
                               options={'quality': 50})
    jpg_image = ImageSpecField(source='original_image',
                                format='JPEG',
                                options={'quality': 50})
    height = models.PositiveSmallIntegerField(blank=True, null=True)
    width = models.PositiveSmallIntegerField(blank=True, null=True)
    search_text = models.TextField(blank=True)
    text_generated_at = models.DateTimeField(blank=True, null=True)
    # sections (MtM)
    # section_headings (OtM)
    # tables (MtM)
    # graphics (MtO)
    kinds = ArrayField(models.CharField(max_length=3, choices=Kind.choices), null=True, blank=True)
    image_problems = ArrayField(models.CharField(max_length=3, choices=ImageProblem.choices), null=True, blank=True)
    text_rotation = models.CharField(max_length=1, blank=True, null=True, default=None, choices=Rotation.choices)

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

    def max_word_height(self):
        words = self.boxes.filter(level=Box.Level.WORD).order_by('-height')
        if words:
            return words[0].height/self.height
        else:
            return None

    def median_word_height(self):
        words = self.boxes.filter(level=Box.Level.WORD).order_by('-height')
        if words:
            middle = len(words)//2
            return words[middle].height/self.height
        else:
            return None

    def generate_text(self):
        word_boxes = self.boxes.filter(level=Box.Level.WORD)
        word_list = [box.text for box in word_boxes]
        text = word_list_to_text(word_list)
        self.search_text = text
        self.save()


class Section(TreeNodeModel, TimeStampedModel):
    treenode_display_field = 'display_name'
    class Kind(models.TextChoices):
        FRONT_MATTER = 'FMA'
        BODY = 'BOD'
        BACK_MATTER = 'BMA'
        CHAPTER = 'CHA'
        CHAPTER_GROUP = 'CHG'
        SUBCHAPTER = 'SUB'
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
        ERRATA = 'ERR'
        EPIGRAPH = 'EPI'
        FOREWORD = 'FOR'
        LIST_OF_TABLES = 'LTA'
        LIST_OF_FIGURES = 'LFI'
        LIST_OF_PLATES = 'LPL'
        LIST_OF_EQUATIONS = 'LEQ'
        OTHER = 'OTH'

    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='sections')
    kind = models.CharField(max_length=3, choices=Kind.choices, blank=True)
    kind_in_book = models.CharField(max_length=15, blank=True)
    title = models.CharField(max_length=100, blank=True)
    number = models.PositiveSmallIntegerField(null=True, blank=True)
    number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    for_edition = models.PositiveSmallIntegerField(null=True, blank=True)
    heading_page = models.ForeignKey(Page, on_delete=models.RESTRICT, related_name='section_headings')
    pages = models.ManyToManyField(Page, blank=True, related_name='sections')
    topics = models.ManyToManyField(Topic, blank=True, related_name='sections')
    contributions = models.ManyToManyField(Contribution, blank=True, related_name='sections')

    def __str__(self):
        return f'{str(self.book)} {self.kind.capitalize()} {self.number}'

    def get_absolute_url(self):
        if self.kind & self.number:
            return f'{self.book.get_absolute_url()}/{self.kind}/{self.number}'
        else:
            return f'{self.book.get_absolute_url()}/section/{self.id}'

    @property
    def display_name(self):
        if self.number:
            return f'{self.Kind(self.kind).label} {self.number}'
        else:
            return self.Kind(self.kind).label

    class Meta:
        ordering = ['heading_page']


class Book(TimeStampedModel):
    class Language(models.TextChoices):
        FRENCH = "FRE"
        GERMAN = "GER"
        LATIN = "LAT"
        GREEK = "GRE"
        INDONESIAN = "IND"

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
    downloaded_at = models.DateTimeField(null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)
    publishing_frequency = models.CharField(max_length=1, choices=PublishingFrequency.choices, blank=True)
    scan_color = models.CharField(max_length=3, choices=Color.choices, blank=True)
    title_page = models.OneToOneField(Page, related_name='title_page_for', on_delete=models.SET_NULL, blank=True, null=True)
    copyright_page = models.OneToOneField(Page, related_name='copyright_page_for', on_delete=models.SET_NULL, blank=True, null=True)
    printing_info_page = models.OneToOneField(Page, related_name='printing_info_page_for', on_delete=models.SET_NULL, blank=True, null=True)
    has_vector_text = models.BooleanField(null=True)
    title = models.CharField(max_length=100, blank=True)
    subtitle = models.TextField(blank=True)
    edition_number = models.PositiveSmallIntegerField(null=True, blank=True)
    volume_number = models.PositiveSmallIntegerField(null=True, blank=True)
    volume_number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    issue_number = models.PositiveSmallIntegerField(null=True, blank=True)
    issue_number_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)
    printing_number = models.PositiveSmallIntegerField(null=True, blank=True)
    numbers_offset = models.PositiveSmallIntegerField(null=True, blank=True)
    roman_numbers_offset = models.PositiveSmallIntegerField(null=True, blank=True)
    in_copyright = models.BooleanField(null=True, blank=True)
    has_ligatures = models.BooleanField(null=True, blank=True)
    cities = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    topics = models.ManyToManyField(Topic, blank=True, related_name='books')
    contributions = models.ManyToManyField(Contribution, blank=True, related_name='books')
    printers = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    publishers = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    copyright_years = ArrayField(models.PositiveSmallIntegerField(), blank=True, null=True)
    # pages (OtM)
    # sections (OtM)
    # graphics (OtM)
    slug = models.SlugField(blank=True, null=True, unique=True)
    hidden = models.BooleanField(blank=True, default=False)
    other_languages = ArrayField(models.CharField(max_length=15, choices=Language.choices), null=True, blank=True)
    series_name = models.CharField(max_length=63, blank=True, null=True)
    number_in_series = models.PositiveSmallIntegerField(blank=True, null=True)
    number_in_series_kind = models.CharField(max_length=1, choices=NumberKind.choices, blank=True)

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
            full_title = full_title + self.title
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
        HALF_TONE = 'HAL'
        # see art of engraving, with the various modes of operation Under the Following Different Divisions: Eching, Soft-ground Etching, Line-engraving, Dhalk and Stipple, Aquatint, Mezzotint, Lithography, Wood Engraving, Medallic Engraving, Electrography, and Photography: Illustrated with Specimens of the Different Styles of Engraving. London: Ackermann and Co., 1841

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
        TABLE = 'TAB'

    class Color(models.TextChoices):
        COLOR = 'COL'
        BITONAL = 'BIT'
        GRAYSCALE = 'GRA'

    class Kind(models.TextChoices):
        FIGURE = 'FIG'
        PLATE = 'PLA'
        EQUATION = 'EQU'
        TABLE = 'TAB'

    medium = models.CharField(max_length=3, choices=Medium.choices, blank=True)
    content = models.CharField(max_length=3, choices=Content.choices, blank=True)
    print_color = models.CharField(max_length=3, choices=Color.choices, blank=True)
    # TODO: change page to non nullable after resetting db
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='graphics', null=True)
    artists = models.ManyToManyField(Person, related_name='graphics')
    caption = models.TextField(blank=True)
    title = models.TextField(blank=True)
    left = models.PositiveSmallIntegerField(null=True, blank=True)
    top = models.PositiveSmallIntegerField(null=True, blank=True)
    width = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    left_with_text = models.PositiveSmallIntegerField(null=True, blank=True)
    top_with_text = models.PositiveSmallIntegerField(null=True, blank=True)
    width_with_text = models.PositiveSmallIntegerField(null=True, blank=True)
    height_with_text = models.PositiveSmallIntegerField(null=True, blank=True)
    kind = models.CharField(max_length=3, blank=True, choices=Kind.choices)
    number = models.PositiveSmallIntegerField(blank=True, null=True)
    number_kind = models.CharField(max_length=1, blank=True, choices=NumberKind.choices)

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

    page = models.ForeignKey(Page, on_delete=models.CASCADE, blank=True, related_name='boxes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    order = models.PositiveIntegerField()
    original_text = models.CharField(max_length=63, blank=True, editable=False)
    text = models.CharField(max_length=63, blank=True)
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
    confirmed_at = models.DateTimeField(blank=True, null=True)
    empty = models.BooleanField(default=False, blank=True)


    class Meta:
        verbose_name_plural = 'boxes'
        ordering = ['order']

    def __str__(self):
        return f'{self.page_number}:{self.block_number}:{self.paragraph_number}:{self.line_number}:{self.word_number}:{self.text}'

    def image_tag(self):
        if not self.level:
            return
        if self.level == self.Level.WORD:
            desired_height = 50
        elif self.level == self.Level.LINE:
            desired_height = 100
        elif self.level == self.Level.PARAGRAPH:
            desired_height = 100
        elif self.level == self.Level.BLOCK:
            desired_height = 100
        elif self.level == self.Level.PAGE:
            desired_height = 100
        scale = desired_height / self.height
        return mark_safe(f'<div style="overflow:hidden;width:{self.width*scale}px;height:{self.height*scale}px;"><img src="{self.page.jpg_image.url}" style="margin-top:-{self.top*scale}px;margin-left:-{self.left*scale}px;transform:scale({scale});transform-origin:0px 0px;"/></div>')

    def get_absolute_url(self):
        return f'{self.page.get_absolute_url()}/box/{self.id}'

    def save(self, *args, **kwargs):
        if self.level == Level.WORD:
            # TODO: test if the word changed before doing this:
            self.page.generate_text()
        super(Box, self).save(*args, **kwargs)


class BookCheck(models.Model):
    class Kind(models.TextChoices):
        SCAN_COLOR = 'SCA'
        HAS_VECTOR_TEXT = 'VEC'
        TITLE_PAGE = 'TIP'
        TITLE = 'TIT'
        SUBTITLE = 'SUB'
        CONTRIBUTIONS = 'CON'
        VOLUME_NUMBER = 'VOL'
        EDITION_NUMBER = 'EDI'
        ISSUE_NUMBER = 'ISS'
        SERIES = 'SER'
        CITIES = 'CIT'
        PUBLISHING_FREQUENCY = 'PUF'
        COPYRIGHT_PAGE = 'COP'
        DATE_PUBLISHED = 'DAT'
        IN_COPYRIGHT = 'INC'
        COPYRIGHT_YEARS = 'COY'
        HAS_LIGATURES = 'LIG'
        PUBLISHERS = 'PUB'
        PRINTING_NUMBER = 'PRN'
        PRINTING_INFO_PAGE = "PIP"
        PRINTERS = 'PRI'
        TOPICS = 'TOP'
        SECTIONS = 'SEC'
        GRAPHICS = 'GRA'
        NUMBERS_OFFSET = 'NUM'
        ROMAN_NUMBERS_OFFSET = 'RNO'
        OTHER_LANGUAGES = 'LAN'

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='checks')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=3, choices=Kind.choices)
    old_value = models.CharField(max_length=127, null=True, blank=True)
    new_value = models.CharField(max_length=127, null=True, blank=True)


class SectionCheck(models.Model):
    class Kind(models.TextChoices):
        KIND = 'KIN'
        KIND_IN_BOOK = 'KIB'
        TITLE = 'TIT'
        NUMBER = 'NUM'
        FOR_EDITION = 'FED'
        FIRST_PAGE = 'FPA'
        LAST_PAGE = 'LPA'
        CONTRIBUTIONS = 'CON'
        TOPICS = 'TOP'

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='checks')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=3, choices=Kind.choices)
    old_value = models.CharField(max_length=127, null=True, blank=True)
    new_value = models.CharField(max_length=127, null=True, blank=True)


class GraphicCheck(models.Model):
    class Kind(models.TextChoices):
        MEDIUM = 'MED'
        CONTENT = 'CON'
        PRINT_COLOR = 'COL'
        PAGES = 'PAG'
        ARTISTS = 'ART'
        CAPTION = 'CAP'
        TITLE = 'TIT'
        BOX = 'BOX'
        BOX_WITH_TEXT = 'BWT'
        KIND = 'KIN'
        NUMBER = 'NUM'

    graphic = models.ForeignKey(Graphic, on_delete=models.CASCADE, related_name='checks')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=3, choices=Kind.choices)
    old_value = models.CharField(max_length=127, null=True, blank=True)
    new_value = models.CharField(max_length=127, null=True, blank=True)


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