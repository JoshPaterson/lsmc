from subprocess import run
import json
import os
from pydantic import BaseModel, PositiveInt, validator, root_validator
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

class Unchecked(object):
    def __bool__(self):
        return False

    def __copy__(self):
        return self

    def __deepcopy__(self, _):
        return self

    def __repr__(self):
        return '<unchecked>'
UNCHECKED = Unchecked()


class Section(BaseModel):
    kind: str = UNCHECKED
    kind_in_book: str = UNCHECKED
    title: str | None = UNCHECKED
    authors: list[str] = UNCHECKED
    number: PositiveInt | None = UNCHECKED
    number_kind: str | None = UNCHECKED
    for_edition: PositiveInt | None = UNCHECKED
    heading_page: PositiveInt = UNCHECKED
    first_page: PositiveInt
    last_page: PositiveInt
    topics: list[str] = UNCHECKED

    class Config:
        alias_generator = to_camel
        validate_assignment = True

    @validator('kind')
    def valid_kind(cls, v):
        if v not in section_kinds:
            raise ValidationError('Invalid value for Section.kind')
        return v

    @validator('number_kind')
    def valid_number_kind(cls, v):
        if v not in number_kinds.union({UNCHECKED, None}):
            raise ValidationError('Invalid value for Section.number_kind')
        return v

    @root_validator
    def last_after_first(cls, values):
        if values['last_page'] < values['first_page']:
            raise ValidationError('last_page cannot be less than first_page')
        return values

    @root_validator
    def heading_in_range(cls, values):
        if values['heading_page'] is not UNCHECKED:
            if not (values['first_page'] <= values['heading_page'] <= values['last_page']):
                raise ValidationError('heading_page must be between first_page and last_page')
        return values


class Plate(BaseModel):
    number: int | None = UNCHECKED
    number_kind: str | None = UNCHECKED
    pages: list[PositiveInt]

    class Config:
        alias_generator = to_camel
        validate_assignment = True

    @validator('number_kind')
    def valid_number_kind(cls, v):
        if v not in number_kinds:
            raise ValidationError('Invalid value for Plate.number_kind')
        return v

class Signature(BaseModel):
    name: str = UNCHECKED
    page: PositiveInt

    class Config:
        alias_generator = to_camel
        validate_assignment = True

class Pdf(BaseModel):
    source_file: str
    url: str | None = UNCHECKED

    authors: list[str] = UNCHECKED
    editors: list[str] = UNCHECKED
    translators: list[str] = UNCHECKED

    date_published: str | None = UNCHECKED
    publishing_frequency: str | None = UNCHECKED

    title: str | None = UNCHECKED
    subtitle: str | None = UNCHECKED
    long_title: str | None = UNCHECKED
    edition: PositiveInt | None = UNCHECKED
    volume: PositiveInt | None = UNCHECKED

    in_copyright: bool | None = UNCHECKED
    copyright_years: list[PositiveInt] = UNCHECKED
    publishers: list[str] = UNCHECKED
    publisher_cities: list[str] = UNCHECKED
    printers: list[str] = UNCHECKED
    printing_number: PositiveInt | None = UNCHECKED

    numbers_offset: PositiveInt | None = UNCHECKED
    roman_numbers_offset: PositiveInt | None = UNCHECKED

    has_ligatures: bool = UNCHECKED

    book_topics: list[str] = UNCHECKED

    blank_pages: list[PositiveInt] = UNCHECKED
    title_pages: list[PositiveInt] = UNCHECKED
    publishing_info_pages: list[PositiveInt] = UNCHECKED
    front_cover_pages: list[PositiveInt] = UNCHECKED
    back_cover_pages: list[PositiveInt] = UNCHECKED
    end_paper_pages: list[PositiveInt] = UNCHECKED
    printing_info_pages: list[PositiveInt] = UNCHECKED
    half_title_pages: list[PositiveInt] = UNCHECKED
    frontispiece_pages: list[PositiveInt] = UNCHECKED
    illustration_pages: list[PositiveInt] = UNCHECKED
    advertisement_partial_pages: list[PositiveInt] = UNCHECKED
    advertisement_full_pages: list[PositiveInt] = UNCHECKED
    photograph_pages: list[PositiveInt] = UNCHECKED

    signatures: list[Signature] = UNCHECKED
    plates: list[Plate] = UNCHECKED
    sections: list[Section] = UNCHECKED

    page_count: int

    # document_id: str
    # instance_id: str
    # metadata_version: str = '0.1'

    class Config:
        validate_assignment = True
        alias_generator = to_camel
        json_encoders = {
            PosixPath: lambda v: str(v),
        }

    @validator('date_published')
    def int_date(cls, v):
        if isinstance(v, int):
            v = str(v) + '-01-01'
        return v

    # TODO: validate that all page numbers are less than PageCount

    @classmethod
    def from_path(cls, pdf_path):
        in_dict = exiftool_read(pdf_path, ['-XMP-smc:all', '-PageCount'])
        for tag in in_dict.get('NullTags', []):
            if tag in list_fields_alias:
                in_dict[tag] = []
            else:
                in_dict[tag] = None
        for tag in in_dict.get('UncheckedTags', []):
            in_dict[tag] = UNCHECKED

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
            elif (field in out_dict) & (out_dict[field] is UNCHECKED):
                unchecked_tags.append(field)
                del out_dict[field]

        if null_tags:
            out_dict['NullTags'] = null_tags

        if unchecked_tags:
            out_dict['UncheckedTags'] = unchecked_tags

        # if 'date_published' in out_dict:
        #     out_dict['date_published'] = out_dict['date_published'].isoformat()


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
        raise_error_if_necessary(returned)

        new_metadata = self.from_path(self.source_file)
        if new_metadata == self:
            os.remove(self.source_file + '_original')
        else:
            os.remove(self.source_file)
            os.rename(self.source_file + '_original', self.source_file)
            raise RuntimeError('PdfMetadata cannot be reproduced after writing with exiftool')

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
