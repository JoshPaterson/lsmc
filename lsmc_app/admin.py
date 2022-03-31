from django.contrib import admin
from .models import City, Book, Topic, CopyrightYear, Page, Section, Author, Editor, Translator, Publisher, Printer, PageKind, Graphic

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

class PageInline(admin.TabularInline):
    model = Page

class SectionInline(admin.TabularInline):
    model = Section

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inline = [PageInline, SectionInline]

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(CopyrightYear)
class CopyrightYearAdmin(admin.ModelAdmin):
    pass

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    pass

@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    pass

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    pass

@admin.register(PageKind)
class PageKindAdmin(admin.ModelAdmin):
    pass

@admin.register(Graphic)
class GraphicKindAdmin(admin.ModelAdmin):
    pass
