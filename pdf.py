from subprocess import run
import json
import os
from pydantic import BaseModel, PositiveInt, validator, root_validator, Field, PrivateAttr
from pydantic.error_wrappers import ValidationError
from pathlib import PosixPath
import uuid


class ExifToolError(RuntimeError):
    pass

def uuid_str():
    return str(uuid.uuid4)

section_kinds = {'introduction', 'acknowledgement', 'dedication', 'preface', 'chapter', 'table', 'appendix', 'glossary', 'index', 'table_of_contents', 'bibliography', 'publishers_catalog', 'appendix', 'article', 'appendices', 'tables', 'chapter_group', 'plates'}

page_kinds = {'blank', 'title', 'publishing_info', 'printing_info', 'front_cover', 'back_cover', 'decorative_paper', 'half_title', 'front_jacket', 'front_jacket_flap', 'back_jacket', 'back_jacket_flap', 'full_ad', 'partial_ad', 'equations'}

number_kinds = {'roman_upper', 'roman_lower', 'arabic', 'letter_upper', 'letter_lower'}

def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))

ineditable_fields = {'source_file', 'page_count'}
ineditable_fields_alias = {to_camel(v) for v in ineditable_fields}

str_fields = {'url', 'date_published', 'publishing_frequency', 'title', 'subtitle', 'long_title'}
bool_fields = {'in_copyright', 'has_ligatures'}
int_fields = {'volume', 'edition', 'printing_number', 'numbers_offset', 'roman_numbers_offset'}
list_fields = {'authors', 'editors', 'translators', 'copyright_years', 'publishers', 'publisher_cities', 'printers', 'book_topics'}
list_fields_alias = {to_camel(i) for i in list_fields}
struct_fields = {'sections', 'graphics', 'page_tags'}

section_str_fields = {'kind', 'kind_in_book', 'title', 'number_kind'}
section_int_fields = {'for_edition', 'first_page', 'last_page', 'heading_page', 'number'}
section_list_fields = {'authors', 'section_topics'}

graphic_str_fields = {'kind', 'content', 'color'}
graphic_int_fields = {'first_page', 'last_page'}

class Unchecked(BaseModel):
    def __bool__(self):
        return False

    def __copy__(self):
        return self

    def __deepcopy__(self, _):
        return self

    def __repr__(self):
        return '<unchecked>'

    def __eq__(self, other):
        return isinstance(other, type(self))
UNCHECKED = Unchecked()


class Section(BaseModel):
    kind: str | Unchecked = UNCHECKED
    kind_in_book: str | Unchecked = UNCHECKED
    title: str | None | Unchecked = UNCHECKED
    authors: list[str] | Unchecked = UNCHECKED
    number: PositiveInt | None | Unchecked = UNCHECKED
    number_kind: str | None | Unchecked = UNCHECKED
    for_edition: PositiveInt | None | Unchecked = UNCHECKED
    heading_page: PositiveInt
    first_page: PositiveInt | Unchecked = UNCHECKED
    last_page: PositiveInt | Unchecked = UNCHECKED
    section_topics: list[str] | Unchecked = UNCHECKED

    page_count: PositiveInt

    class Config:
        alias_generator = to_camel
        validate_assignment = True

    @validator('kind')
    def valid_kind(cls, v):
        if v == UNCHECKED:
            return v
        if v not in section_kinds:
            raise ValidationError('Invalid value for Section.kind')
        return v

    @validator('number_kind')
    def valid_number_kind(cls, v):
        if v == UNCHECKED or v is None:
            return v
        if v not in number_kinds:
            raise ValidationError('Invalid value for Section.number_kind')
        return v

    @validator('heading_page', 'for_edition', 'number', 'number_kind', 'kind', 'kind_in_book', 'title', 'first_page', 'last_page', pre=True)
    def not_empty_sequence(cls, v):
        if isinstance(v, list | tuple | set | str) and len(v) == 0:
            raise ValidationError('Cannot be an empty sequence')
        return v

    @validator('authors', 'section_topics')
    def does_not_contain_empty_string(cls, v):
        for i in v:
            if i == '':
                raise ValidationError('Empty string is invalid')
        return v

    @root_validator
    def first_before_heading(cls, values):
        if values['first_page'] != UNCHECKED and values['first_page'] > values['heading_page']:
            raise ValidationError('first_page must be before heading_page')
        return values

    @root_validator
    def last_after_heading(cls, values):
        if values['last_page'] != UNCHECKED and values['last_page'] < values['heading_page']:
            raise ValidationError('last_page must be after heading_page')
        return values

    @root_validator
    def page_numbers_lt_page_count(cls, values):
        for field in ['heading_page', 'first_page', 'last_page']:
            if values[field] and values[field] > values['page_count']:
                raise ValidationError(f'{field} cannot be higher than page_count')
        return values

    def __getitem__(self, item):
        return getattr(self, item)


class Graphic(BaseModel):
    kind: str | None | Unchecked = UNCHECKED
    content: str | None | Unchecked = UNCHECKED
    first_page: PositiveInt
    last_page: PositiveInt | Unchecked = UNCHECKED
    color: str | Unchecked = UNCHECKED

    page_count: PositiveInt

    class Config:
        alias_generator = to_camel
        validate_assignment = True

    def __getitem__(self, item):
        return getattr(self, item)

    @validator('kind', 'content', 'color', 'last_page', pre=True)
    def not_empty_sequence(cls, v):
        if isinstance(v, list | tuple | set | str) and len(v) == 0:
            raise ValidationError('Cannot be an empty sequence')
        return v

    @root_validator
    def last_page_after_first(cls, values):
        if values['last_page'] and values['first_page'] > values['last_page']:
            raise ValidationError('last_page must be after first_page')
        return values

    @root_validator
    def page_numbers_lt_page_count(cls, values):
        for field in ['first_page', 'last_page']:
            if values[field] and values[field] > values['page_count']:
                raise ValidationError(f'{field} cannot be higher than page_count')
        return values


class PageTag(BaseModel):
    kind: str
    pages: list[PositiveInt] = []

    page_count: PositiveInt

    class Config:
        alias_generator = to_camel
        validate_assignment = True

    def __getitem__(self, item):
        return getattr(self, item)

    @root_validator
    def page_numbers_lt_page_count(cls, values):
        if values['pages'] and max(values['pages']) > values['page_count']:
            raise ValidationError('pages cannot be higher than page_count')
        return values

    @validator('kind', pre=True)
    def not_empty_sequence(cls, v):
        if isinstance(v, list | tuple | set | str) and len(v) == 0:
            raise ValidationError('Cannot be an empty sequence')
        return v



class Pdf(BaseModel):
    source_file: str
    url: str | None | Unchecked = UNCHECKED

    authors: list[str] | Unchecked = UNCHECKED
    editors: list[str] | Unchecked = UNCHECKED
    translators: list[str] | Unchecked = UNCHECKED

    date_published: str | None | Unchecked = UNCHECKED
    publishing_frequency: str | None | Unchecked = UNCHECKED

    title: str | None | Unchecked = UNCHECKED
    subtitle: str | None | Unchecked = UNCHECKED
    long_title: str | None | Unchecked = UNCHECKED
    edition: PositiveInt | None | Unchecked = UNCHECKED
    volume: PositiveInt | None | Unchecked = UNCHECKED

    in_copyright: bool | None | Unchecked = UNCHECKED
    copyright_years: list[PositiveInt] | Unchecked = UNCHECKED
    publishers: list[str] | Unchecked = UNCHECKED
    publisher_cities: list[str] | Unchecked = UNCHECKED
    printers: list[str] | Unchecked = UNCHECKED
    printing_number: PositiveInt | None | Unchecked = UNCHECKED

    numbers_offset: PositiveInt | None | Unchecked = UNCHECKED
    roman_numbers_offset: PositiveInt | None | Unchecked = UNCHECKED

    has_ligatures: bool | Unchecked = UNCHECKED

    book_topics: list[str] | Unchecked = UNCHECKED

    page_tags: list[PageTag] | Unchecked = UNCHECKED
    graphics: list[Graphic] | Unchecked = UNCHECKED
    sections: list[Section] | Unchecked = UNCHECKED

    page_count: int

    class Config:
        validate_assignment = True
        alias_generator = to_camel

    @validator('date_published', pre=True)
    def int_date(cls, v):
        if isinstance(v, int):
            v = str(v) + '-01-01'
        return v

    @root_validator
    def page_numbers_lt_page_count(cls, values):
        for field in ['numbers_offset', 'roman_numbers_offset']:
            if values[field] and values[field] > values['page_count']:
                raise ValidationError(f'{field} cannot be higher than page_count')
        return values

    @validator('url', 'date_published', 'publishing_frequency', 'title', 'subtitle', 'long_title')
    def is_not_empty_string(cls, v):
        if v == '':
            raise ValidationError('Empty string is invalid')
        return v

    @validator('authors', 'editors', 'translators', 'publishers', 'publisher_cities', 'printers', 'book_topics')
    def does_not_contain_empty_string(cls, v):
        for i in v:
            if i == '':
                raise ValidationError('Empty string is invalid')
        return v

    @validator('url', 'date_published', 'publishing_frequency', 'title', 'subtitle', 'long_title', 'edition', 'volume', 'printing_number', 'numbers_offset', 'roman_numbers_offset',  'in_copyright', 'has_ligatures', pre=True)
    def not_empty_sequence(cls, v):
        if isinstance(v, list | tuple | set | str) and len(v) == 0:
            raise ValidationError('Cannot be an empty sequence')
        return v

    @validator('sections', 'graphics', 'page_tags', pre=True)
    def list_not_contain_empty_sequence(cls, v):
        if isinstance(v, list | set | tuple):
            for empty_seq in [[], '', (), {}]:
                if empty_seq in v:
                    raise ValidationError('Cannot initialize section with empty sequence')
        return v

    def __getitem__(self, item):
        return getattr(self, item)

    @classmethod
    def from_path(cls, pdf_path):
        in_dict = exiftool_read(pdf_path, ['-XMP-lsmc:all', '-PageCount'])
        if 'NullTags' in in_dict:
            for tag in in_dict['NullTags']:
                if tag in list_fields_alias:
                    in_dict[tag] = []
                else:
                    in_dict[tag] = None
            del in_dict['NullTags']

        if 'UncheckedTags' in in_dict:
            for tag in in_dict['UncheckedTags']:
                in_dict[tag] = UNCHECKED
            del in_dict['UncheckedTags']

        return cls(**in_dict)

    def editable_fields(self):
        fields = []
        for k, v in self:
            fields.append(to_camel(k))

        for tag in ineditable_fields_alias:
            fields.remove(tag)
        return fields

    def exiftool_dict(self) -> dict:
        out_dict = self.dict(by_alias=True, exclude=ineditable_fields)

        null_tags = []
        unchecked_tags = []

        for field in self.editable_fields():
            if (field in out_dict) & (out_dict[field] in [None, []]):
                null_tags.append(field)
                del out_dict[field]
            elif (field in out_dict) & (out_dict[field] == UNCHECKED):
                unchecked_tags.append(field)
                del out_dict[field]

        if null_tags:
            out_dict['NullTags'] = null_tags

        if unchecked_tags:
            out_dict['UncheckedTags'] = unchecked_tags

        out_dict = {f'XMP-lsmc:{k}':v for k,v in out_dict.items()}
        out_dict.update({'SourceFile': self.source_file})
        return out_dict

    def write(self):
        out_dict = self.exiftool_dict()

        params = []
        for tag in out_dict.get('XMP-lsmc:NullTags', []):
            params.append(f'-XMP-lsmc:{tag}=')
        for tag in out_dict.get('XMP-lsmc:UncheckedTags', []):
            params.append(f'-XMP-lsmc:{tag}=')

        temp_file = '.temp.json'
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(out_dict, f, ensure_ascii=False)
        params = ['exiftool', '-config', '.ExifTool_config', f'-json={temp_file}'] + params + [str(self.source_file)]
        returned = run(params, capture_output=True)
        os.remove(temp_file)
        if b'0 image files updated' in returned.stderr:
            raise ExifToolError(f'Exiftool exited with a return code of {returned.returncode}: {returned.stderr.decode()}')
        raise_error_if_necessary(returned)
        try:
            new_metadata = self.from_path(self.source_file)
        except ValidationError:
            os.remove(self.source_file)
            os.rename(self.source_file + '_original', self.source_file)
            raise RuntimeError('Metadata cannot be parsed after writing')

        if new_metadata == self:
            os.remove(self.source_file + '_original')
        else:
            os.remove(self.source_file)
            os.rename(self.source_file + '_original', self.source_file)
            raise RuntimeError('Metadata is parsed after writing but does not match')

    def repair_xmp(self):
        params = ['exiftool', '-config', '.ExifTool_config', '-xmp:all=', '-tagsfromfile', '@', '-xmp:all', str(self.source_file)]
        # https://exiftool.org/forum/index.php?topic=9094.0



def raise_error_if_necessary(returned):
    if b'Warning' in returned.stderr or returned.returncode != 0:
        raise ExifToolError(f'Exiftool exited with a return code of {returned.returncode}: {returned.stderr.decode()}')


def exiftool_read(pdf_path, tags):
    params = ['exiftool', '-config', '.ExifTool_config', '-j', '-struct'] + tags + [str(pdf_path)]
    returned = run(params, capture_output=True)
    raise_error_if_necessary(returned)
    return json.loads(returned.stdout.decode())[0]
