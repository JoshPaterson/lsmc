from pprint import pprint
from sqlite3 import paramstyle
from subprocess import run
import json
import os
from tempfile import tempdir
from enum import Enum, auto
from pydantic import BaseModel, HttpUrl, FilePath, PastDate, PositiveInt, validator
from typing import Optional, Any
from pathlib import PosixPath


class ExifToolError(RuntimeError):
    pass

section_kinds = {'introduction', 'acknowledgement', 'dedication', 'preface', 'chapter', 'chapter_group', 'table', 'signature', 'appendix', 'glossary', 'index', 'table_of_contents', 'bibliography', 'publishers_catalog'}

def to_camel(string: str) -> str:
    return ''.join(word.capitalize() for word in string.split('_'))

ineditable_fields = {'source_file', 'page_count'}
ineditable_fields_alias = {to_camel(v) for v in ineditable_fields}

number_kinds = {'roman_upper', 'roman_lower', 'arabic', 'letter_upper', 'letter_lower'}

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


class PageGroup(BaseModel):
    kind: str
    title: str = None
    number: str = None
    number_kind: PositiveInt = None
    for_edition: PositiveInt = None
    first_page: PositiveInt
    last_page: PositiveInt
    except_pages: list[PositiveInt] = None
    topics: list[str] = None

    class Config:
        alias_generator = to_camel

    @validator('kind')
    def valid_option(cls, v):
        if v not in section_kinds:
            raise ValueError('Invalid kind of PageGroup')
        return v


class PdfMetadata(BaseModel):
    source_file: str
    url: str = None

    authors: list[str] = UNCHECKED
    editors: list[str] = UNCHECKED
    translators: list[str] = UNCHECKED

    date_published: str = UNCHECKED
    frequency: str = UNCHECKED

    title: str = UNCHECKED
    subtitle: str = None
    long_title: str = None
    edition: PositiveInt = UNCHECKED
    volume: PositiveInt = UNCHECKED

    in_copyright: bool = UNCHECKED
    copyright_years: list[PositiveInt] = UNCHECKED
    publishers: list[str] = UNCHECKED
    publisher_cities: list[str] = UNCHECKED
    printers: list[str] = UNCHECKED
    printing_number: PositiveInt = UNCHECKED

    numbers_offset: PositiveInt = UNCHECKED
    roman_numbers_offset: PositiveInt = UNCHECKED

    has_ligatures: bool = UNCHECKED

    book_topics: list[str] = UNCHECKED

    page_groups: list[PageGroup] = None

    blank_pages: list[PositiveInt] = UNCHECKED
    title_pages: list[PositiveInt] = UNCHECKED
    publishing_info_pages: list[PositiveInt] = UNCHECKED
    front_cover_pages: list[PositiveInt] = UNCHECKED
    back_cover_pages: list[PositiveInt] = UNCHECKED
    end_paper_pages: list[PositiveInt] = UNCHECKED
    printing_info_pages: list[PositiveInt] = UNCHECKED
    half_title_pages: list[PositiveInt] = UNCHECKED
    frontispiece_pages: list[PositiveInt] = UNCHECKED
    plate_pages: list[PositiveInt] = UNCHECKED
    illustration_pages: list[PositiveInt] = UNCHECKED
    advertisement_pages: list[PositiveInt] = UNCHECKED

    page_count: int

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

    @classmethod
    def from_pdf(cls, pdf_path):
        in_dict = exiftool_read(pdf_path, ['-XMP-smc:all', '-PageCount'])
        for tag in in_dict.get('null_tags', []):
            in_dict[tag] = None
        for tag in in_dict.get('unknown_tags', []):
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
            if (field in out_dict) & (out_dict[field] is None):
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

        new_metadata = PdfMetadata.from_pdf(self.source_file)
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
