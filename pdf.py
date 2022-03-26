from subprocess import run
import json
import os
from pydantic import BaseModel, PositiveInt, validator, root_validator, Field
from pydantic.error_wrappers import ValidationError
from pathlib import PosixPath
import uuid


class ExifToolError(RuntimeError):
    pass

def uuid_str():
    return str(uuid.uuid4)

section_kinds = {'introduction', 'acknowledgement', 'dedication', 'preface', 'chapter', 'table', 'appendix', 'glossary', 'index', 'table_of_contents', 'bibliography', 'publishers_catalog', 'appendix', 'article', 'appendices', 'tables', 'chapter_group', 'plates'}

def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))

ineditable_fields = {'source_file', 'page_count'}
ineditable_fields_alias = {to_camel(v) for v in ineditable_fields}

number_kinds = {'roman_upper', 'roman_lower', 'arabic', 'letter_upper', 'letter_lower'}

list_fields = {'authors', 'editors', 'translators', 'copyright_years', 'publishers', 'publisher_cities', 'printers', 'book_topics', 'page_groups', 'blank_pages', 'title_pages', 'publishing_info_pages', 'front_cover_pages', 'back_cover_pages', 'end_paper_pages', 'printing_info_pages', 'half_title_pages', 'frontispiece_pages', 'illustration_pages', 'advertisement_partial_pages', 'advertisement_full_pages', 'photograph_pages'}

list_fields_alias = {to_camel(i) for i in list_fields}

struct_fields = {'sections', 'signatures', 'plates'}

class Unchecked(BaseModel):
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
    topics: list[str] | Unchecked = UNCHECKED

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

    @validator('authors', 'topics')
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


class Plate(BaseModel):
    number: int | None | Unchecked = UNCHECKED
    number_kind: str | None | Unchecked = UNCHECKED
    pages: list[PositiveInt] = Field(min_items=1)

    class Config:
        alias_generator = to_camel
        validate_assignment = True

    @validator('number_kind')
    def valid_number_kind(cls, v):
        if v is None or v == UNCHECKED:
            return v
        if v not in number_kinds:
            raise ValidationError('Invalid value for Plate.number_kind')
        return v

    @validator('number', 'number_kind', pre=True)
    def not_empty_sequence(cls, v):
        if isinstance(v, list | tuple | set | str) and len(v) == 0:
            raise ValidationError('Cannot be an empty sequence')
        return v

class Signature(BaseModel):
    name: str | Unchecked = UNCHECKED
    page: PositiveInt

    class Config:
        alias_generator = to_camel
        validate_assignment = True

    @validator('name', pre=True)
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

    blank_pages: list[PositiveInt] | Unchecked = UNCHECKED
    title_pages: list[PositiveInt] | Unchecked = UNCHECKED
    publishing_info_pages: list[PositiveInt] | Unchecked = UNCHECKED
    front_cover_pages: list[PositiveInt] | Unchecked = UNCHECKED
    back_cover_pages: list[PositiveInt] | Unchecked = UNCHECKED
    end_paper_pages: list[PositiveInt] | Unchecked = UNCHECKED
    printing_info_pages: list[PositiveInt] | Unchecked = UNCHECKED
    half_title_pages: list[PositiveInt] | Unchecked = UNCHECKED
    frontispiece_pages: list[PositiveInt] | Unchecked = UNCHECKED
    illustration_pages: list[PositiveInt] | Unchecked = UNCHECKED
    advertisement_partial_pages: list[PositiveInt] | Unchecked = UNCHECKED
    advertisement_full_pages: list[PositiveInt] | Unchecked = UNCHECKED
    photograph_pages: list[PositiveInt] | Unchecked = UNCHECKED

    signatures: list[Signature] | Unchecked = UNCHECKED
    plates: list[Plate] | Unchecked = UNCHECKED
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
        """This fixes what appears to be a bug"""
        if isinstance(v, list | tuple | set | str) and len(v) == 0:
            raise ValidationError('Cannot be an empty sequence')
        return v


    @classmethod
    def from_path(cls, pdf_path):
        in_dict = exiftool_read(pdf_path, ['-XMP-smc:all', '-PageCount'])
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

        out_dict = {f'XMP-smc:{k}':v for k,v in out_dict.items()}
        out_dict.update({'SourceFile': self.source_file})
        return out_dict

    def write(self):
        out_dict = self.exiftool_dict()

        params = []
        for tag in out_dict.get('XMP-smc:NullTags', []):
            params.append(f'-XMP-smc:{tag}=')
        for tag in out_dict.get('XMP-smc:UncheckedTags', []):
            params.append(f'-XMP-smc:{tag}=')

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
