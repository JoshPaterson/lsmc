from django.contrib import admin
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm
from .models import City, Book, Topic, CopyrightYear, Page, Section, Creator, Publisher, Printer, PageKind, Graphic

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
class TopicAdmin(TreeNodeModelAdmin):
    tree_node_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm

@admin.register(CopyrightYear)
class CopyrightYearAdmin(admin.ModelAdmin):
    pass

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass

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

@admin.register(Graphic)
class GraphicKindAdmin(admin.ModelAdmin):
    pass
