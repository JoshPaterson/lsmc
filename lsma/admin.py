from django.contrib import admin
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm
from .models import Book, Topic, Page, Section, Person, Graphic, Box, OcrFix, BookCheck, SectionCheck, GraphicCheck

@admin.register(OcrFix)
class OcrFixAdmin(admin.ModelAdmin):
    pass



@admin.register(Graphic)
class GraphicAdmin(admin.ModelAdmin):
    pass


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_published'
    fieldsets = (
        ('Title', {
            'fields': (('title', 'subtitle'), ('volume_number', 'volume_number_kind'), ('issue_number', 'issue_number_kind'), ('edition_number',), ('series_name', 'number_in_series', 'number_in_series_kind'))
        }),
        ('People', {
            'fields': ('contributions',)
        }),
        ('Title/ Copyright Pages', {
            'fields': ('title_page', 'copyright_page')
        }),
        ('Topics', {
            'fields': ('topics',)
        }),
        ('Book', {
            'fields': ('has_vector_text', 'has_ligatures', 'scan_color', 'numbers_offset', 'roman_numbers_offset', 'other_languages')
        }),
        ('Other', {
            'fields': ('slug', 'uuid', 'url', 'downloaded_at', 'hidden')
        }),
        ('Date', {
            'fields': ('date_published', 'in_copyright', 'publishing_frequency')
        }),
        ('Printing', {
            'fields': ('printing_number', 'copyright_years', 'printers')
        }),
        ('Publisher', {
            'fields': ('publishers', 'cities')
        }),
    )
    readonly_fields = ('slug', 'uuid', 'downloaded_at')
    date_hierarchy = 'date_published'
    filter_horizontal = ['contributions', 'topics']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['title_page', 'copyright_page']:
            book_id = request.resolver_match.kwargs.get('object_id')
            kwargs['queryset'] = Page.objects.filter(book=book_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BookCheck)
class BookCheckAdmin(admin.ModelAdmin):
    pass


@admin.register(SectionCheck)
class SectionCheckAdmin(admin.ModelAdmin):
    pass


@admin.register(GraphicCheck)
class GraphicCheckAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(TreeNodeModelAdmin):
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    fields = ('image_tag', 'thumbnail_tag', 'original_image', 'book', 'number', 'topics', 'graphics', 'text', 'text_generated_at', 'kinds', 'image_problems', 'text_top_rotated_to', 'max_word_height', 'median_word_height')
    readonly_fields = ('image_tag', 'thumbnail_tag', 'max_word_height', 'median_word_height')
    list_display = ['book', 'number', 'thumbnail_tag']
    list_per_page = 20


@admin.register(Section)
class SectionAdmin(TreeNodeModelAdmin):
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


class BoxInline(admin.TabularInline):
    model = Box
    fields = ('image_tag', 'page', 'level', 'order', 'original_text', 'text', '__str__')
    readonly_fields = ('image_tag', 'page', 'level', 'order', 'original_text', 'text', '__str__')
    extra = 0
    show_change_link = True
    view_on_site = False

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    fields = ('page', 'original_text',  'image_tag', 'text', 'parent', 'page_number', 'block_number', 'paragraph_number', 'line_number', 'word_number', 'level', 'left', 'top', 'width', 'height', 'original_confidence', 'order')
    list_display = ('level', 'image_tag', 'text', 'original_confidence')
    readonly_fields = ('image_tag', 'page', 'original_text', 'original_confidence', 'parent', 'page_number', 'block_number', 'paragraph_number', 'line_number', 'word_number', 'level', 'left', 'top', 'width', 'height', 'order')
    list_filter = ['level']
    search_field = ['text', 'original_text']
    empty_value_display = "<empty>"
    list_per_page = 30
    inlines = (BoxInline,)