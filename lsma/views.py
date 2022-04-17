from django.shortcuts import render, redirect
from .models import Book, Section, Graphic
from django.db.models import Count
from django.views.generic import TemplateView

from .forms import PageChoiceForm

class IndexView(TemplateView):
    template_name = 'lsma/index.html'
    def get(self, request):
        book_counts = Book.objects.aggregate(
            # automatic
            Count('scan_color_checked'),
            Count('has_vector_text_checked'),
            # bibliographic
            Count('title_page_checked'),
            Count('title_checked'),
            Count('subtitle_checked'),
            Count('contributions_checked'),
            Count('volume_number_checked'),
            Count('edition_number_checked'),
            Count('issue_number_checked'),
            Count('series_checked'),
            Count('cities_checked'),
            Count('publishing_frequency_checked'),
            Count('copyright_page_checked'),
            Count('date_published_checked'),
            Count('in_copyright_checked'),
            Count('copyright_years_checked'),
            Count('has_ligatures_checked'),
            Count('publishers_checked'),
            Count('printing_number_checked'),
            Count('printing_info_page_checked'),
            Count('printers_checked'),
            Count('topics_checked'),
            # sections
            Count('sections_checked'),
            # graphics
            Count('graphics_checked'),
            # other
            Count('numbers_offset_checked'),
            Count('roman_numbers_offset_checked'),
            Count('other_languages_checked'),
        )
        section_counts = Section.objects.aggregate(
            Count('kind_checked'),
            Count('kind_in_book_checked'),
            Count('title_checked'),
            Count('number_checked'),
            Count('for_edition_checked'),
            Count('first_page_checked'),
            Count('last_page_checked'),
            Count('contributions_checked'),
            Count('topics_checked'),
        )
        graphic_counts = Graphic.objects.aggregate(
            Count('medium_checked'),
            Count('content_checked'),
            Count('print_color_checked'),
            Count('pages_checked'),
            Count('artists_checked'),
            Count('caption_checked'),
            Count('title_checked'),
            Count('box_checked'),
            Count('box_with_text_checked'),
            Count('section_kind_checked'),
            Count('section_number_checked'),

        )
        context = {
            'book_count': Book.objects.count(),
            'book_counts': book_counts,
            'section_counts': section_counts,
            'graphic_counts': graphic_counts,
        }
        return render(request, self.template_name, context)


class EditTitlePageView(TemplateView):
    form_class = PageChoiceForm

    def get(self, request):
        initial = {}
        book = Book.objects.filter(title_page__isnull=True).first()
        pages = book.pages.all()[:20]
        form = self.form_class(pages=pages)
        book = Book.objects.filter(title_page__isnull=True).first()
        return render(request, f'lsma/edit/title-page.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # process data here
            return redirect('/edit/title-page')
