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
        context = {
            'book': book,
            'pages': book.pages.all()[:20],
            'heading': 'Choose Title Page',
            'post_url': '/edit/title-page',
            'page_title': 'Title Page',
        }
        return render(request, f'lsma/edit/choose-1-page.html', context=context)

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
        context = {
            'book': book,
            'pages': book.pages.all()[:20],
            'heading': 'Choose Copyright Page',
            'post_url': '/edit/copyright-page',
            'page_title': 'Copyright Page',
        }
        return render(request, f'lsma/edit/choose-1-page.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.copyright_page
        page = book.pages.get(number=request.POST['page_number'])
        book.copyright_page = page
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.COPYRIGHT_PAGE,
            old_value=old_value,
            new_value=request.POST['page_number'])
        return redirect('/edit/copyright-page')


class EditTitleView(TemplateView):
    def get(self, request):
        book = Book.objects.filter(title='', title_page__isnull=False).first()
        if book == None:
            return redirect('/')
        title_page = book.title_page
        context = {
            'page_title': 'Title',
            'heading': 'Enter Title',
            'image_url': book.title_page.jpg_image.url,
            'post_url': '/edit/title',
            'label': 'Title',
            'book_uuid': book.uuid,
            'previous_value': book.title,
        }
        return render(request, f'lsma/edit/single-text.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.title
        book.title = request.POST['text']
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.TITLE,
            old_value=old_value,
            new_value=request.POST['text']
        )
        return redirect('/edit/title')


class EditSubtitleView(TemplateView):
    def get(self, request):
        book = Book.objects.exclude(checks__kind=BookCheck.Kind.SUBTITLE).filter(title_page__isnull=False).first()
        if book == None:
            return redirect('/')
        context = {
            'page_title': 'Subtitle',
            'heading': 'Enter Subtitle',
            'image_url': book.title_page.jpg_image.url,
            'post_url': '/edit/subtitle',
            'label': 'Subtitle',
            'book_uuid': book.uuid,
            'previous_value': book.subtitle,
        }
        return render(request, f'lsma/edit/single-text.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.subtitle
        book.subtitle = request.POST['text']
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.SUBTITLE,
            old_value=old_value,
            new_value=request.POST['text']
        )
        return redirect('/edit/subtitle')