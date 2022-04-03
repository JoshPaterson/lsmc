from django.contrib import admin
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm
from .models import City, Book, Topic, CopyrightYear, Page, Section, Creator, Publisher, Printer, PageKind, Graphic, Box

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

class PageInline(admin.StackedInline):
    model = Page
    extra = 0
    can_delete = False

class SectionInline(admin.StackedInline):
    model = Section
    extra = 0

class GraphicInline(admin.StackedInline):
    model = Graphic
    extra = 0

@admin.register(Graphic)
class GraphicKindAdmin(admin.ModelAdmin):
    pass

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # inlines = [PageInline, SectionInline, GraphicInline]
    date_hierarchy = 'date_published'
    fieldsets = (
        ('Title', {
            'fields': (('title', 'title_checked'), ('subtitle', 'subtitle_checked'), ('volume_number','volume_number_checked'), ('volume_number_kind', 'volume_number_kind_checked'), ('issue_number','issue_number_checked'), ('issue_number_kind', 'issue_number_kind_checked'), ('edition_number','edition_number_checked'))
        }),
        ('Creators', {
            'fields': (('authors', 'editors', 'translators'), 'creators_checked')
        }),
        ('Title/ Copyright Pages', {
            'fields': (('title_page', 'title_page_checked'), ('copyright_page', 'copyright_page_checked'))
        }),
        ('Topics', {
            'fields': ('topics', 'topics_checked')
        }),
        ('Book', {
            'fields': (('has_vector_text', 'has_vector_text_checked'), ('has_ligatures', 'has_ligatures_checked'), ('scan_color', 'scan_color_checked'), ('numbers_offset', 'numbers_offset_checked'), ('roman_numbers_offset', 'roman_numbers_offset_checked'))
        }),
        ('Other', {
            'fields': ('slug', 'uuid', 'url', 'downloaded_at')
        }),
        ('Date', {
            'fields': (('date_published', 'date_published_checked'), ('in_copyright', 'in_copyright_checked'),('publishing_frequency', 'publishing_frequency_checked'))
        }),
        ('Printing', {
            'fields': (('printing_number', 'printing_number_checked'), ('copyright_years', 'copyright_years_checked'), ('printers', 'printers_checked'))
        }),
        ('Publisher', {
            'fields': (('publishers', 'publishers_checked'), ('cities', 'cities_checked'))
        }),
    )
    readonly_fields = ('slug', 'uuid', 'downloaded_at')
    date_hierarchy = 'date_published'
    filter_horizontal = ['authors', 'translators', 'editors', 'topics', 'copyright_years', 'printers', 'publishers', 'cities']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['title_page', 'copyright_page']:
            book_id = request.resolver_match.kwargs.get('object_id')
            kwargs['queryset'] = Page.objects.filter(book=book_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Topic)
class TopicAdmin(TreeNodeModelAdmin):
    tree_node_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm

@admin.register(CopyrightYear)
class CopyrightYearAdmin(admin.ModelAdmin):
    pass

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fields = ('image_tag',)
    readonly_fields = ('image_tag',)
    list_display = ['book', 'number']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass

@admin.register(Creator)
class AuthorAdmin(admin.ModelAdmin):
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

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('text', 'page_number', 'block_number', 'paragraph_number', 'line_number', 'word_number','level')
    readonly_fields = ('page',)
    list_filter = ['level', 'page_number', 'block_number', 'paragraph_number', 'line_number', 'word_number']
    search_field = ['text', 'original_text']
    empty_value_display = "''"