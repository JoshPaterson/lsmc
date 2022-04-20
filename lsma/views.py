from django.shortcuts import render, redirect
from .models import Book, Section, Graphic, BookCheck, GraphicCheck, SectionCheck
from django.db.models import Count, Q
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'lsma/index.html'
    def get(self, request):
        book_check_counts = BookCheck.objects.all().values('kind').annotate(Count('book', distinct=True))
        book_check_counts = {BookCheck.Kind(d['kind']).name: d['book__count'] for d in book_check_counts}

        section_check_counts = SectionCheck.objects.all().values('kind').annotate(Count('section', distinct=True))
        section_check_counts = {SectionCheck.Kind(d['kind']).name: d['section__count'] for d in section_check_counts}

        graphic_check_counts = GraphicCheck.objects.all().values('kind').annotate(Count('graphic', distinct=True))
        graphic_check_counts = {GraphicCheck.Kind(d['kind']).name: d['graphic__count'] for d in graphic_check_counts}

        context = {
            'book_count': Book.objects.count(),
            'section_count': Section.objects.count(),
            'graphic_count': Graphic.objects.count(),
            'book_check_counts': book_check_counts,
            'section_check_counts': section_check_counts,
            'graphic_check_counts': graphic_check_counts,
        }
        return render(request, self.template_name, context)


class EditTitlePageView(TemplateView):

    def get(self, request):
        book = Book.objects.filter(title_page__isnull=True).first()
        pages = book.pages.all()[:20]
        return render(request, f'lsma/edit/title-page.html', {'book': book, 'pages': pages})

    def post(self, request, *args, **kwargs):
        # process data here
        return redirect('/edit/title-page')
