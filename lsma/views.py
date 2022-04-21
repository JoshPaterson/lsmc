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
        if book == None:
            return redirect('/')
        pages = book.pages.all()[:20]
        return render(request, f'lsma/edit/title-page.html', {'book': book, 'pages': pages})

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.title_page
        page = book.pages.get(number=request.POST['page_number'])
        book.title_page = page
        book.save()
        BookCheck.objects.create(book=book, user=request.user, kind=BookCheck.Kind.TITLE_PAGE, old_value=old_value, new_value=request.POST['page_number'])

        return redirect('/edit/title-page')


class EditCopyrightPageView(TemplateView):
    def get(self, request):
        book = Book.objects.filter(copyright_page__isnull=True).first()
        if book == None:
            return redirect('/')
        pages = book.pages.all()[:20]
        return render(request, f'lsma/edit/copyright-page.html', {'book': book, 'pages': pages})

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.copyright_page
        page = book.pages.get(number=request.POST['page_number'])
        book.copyright_page = page
        book.save()
        BookCheck.objects.create(book=book, user=request.user, kind=BookCheck.Kind.COPYRIGHT_PAGE, old_value=old_value, new_value=request.POST['page_number'])
        return redirect('/edit/copyright-page')


class EditTitleView(TemplateView):
    def get(self, request):
        book = Book.objects.filter(title='', title_page__isnull=False).first()
        if book == None:
            return redirect('/')
        title_page = book.title_page
        return render(request, f'lsma/edit/title.html', {'book': book})

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.title
        book.title = request.POST['title']
        book.save()
        BookCheck.objects.create(book=book, user=request.user, kind=BookCheck.Kind.TITLE, old_value=old_value, new_value=request.POST['title'])
        return redirect('/edit/title')


class EditSubtitleView(TemplateView):
    def get(self, request):
        book = Book.objects.exclude(checks__kind=BookCheck.Kind.SUBTITLE).filter(title_page__isnull=False).first()
        if book == None:
            return redirect('/')
        return render(request, f'lsma/edit/subtitle.html', {'book': book})

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.subtitle
        book.subtitle = request.POST['subtitle']
        book.save()
        BookCheck.objects.create(book=book, user=request.user, kind=BookCheck.Kind.SUBTITLE, old_value=old_value, new_value=request.POST['subtitle'])
        return redirect('/edit/subtitle')