from django.shortcuts import render, redirect
from .models import Book, Section, Graphic, BookCheck, GraphicCheck, SectionCheck
from django.db.models import Count, Q
from django.views.generic import TemplateView
from collections import defaultdict

class IndexView(TemplateView):
    template_name = 'lsma/index.html'
    def get(self, request):
        book_count = Book.objects.count()
        book_check_counts = BookCheck.objects.all().values('kind').annotate(Count('book', distinct=True))
        book_check_counts = {BookCheck.Kind(d['kind']).name: book_count - d['book__count'] for d in book_check_counts}
        book_check_counts = defaultdict(lambda : book_count, book_check_counts)

        section_count = Section.objects.count()
        section_check_counts = SectionCheck.objects.all().values('kind').annotate(Count('section', distinct=True))
        section_check_counts = {SectionCheck.Kind(d['kind']).name: section_count - d['section__count'] for d in section_check_counts}
        section_check_counts = defaultdict(lambda : section_count, section_check_counts)

        graphic_count = Graphic.objects.count()
        graphic_check_counts = GraphicCheck.objects.all().values('kind').annotate(Count('graphic', distinct=True))
        graphic_check_counts = {GraphicCheck.Kind(d['kind']).name: graphic_count - d['graphic__count'] for d in graphic_check_counts}
        graphic_check_counts = defaultdict(lambda : graphic_count, graphic_check_counts)

        context = {
            'book_count': book_count,
            'section_count': section_count,
            'graphic_count': graphic_count,
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
            'input_type': 'text',
            'page_number': book.title_page.number,
        }
        return render(request, f'lsma/edit/single-input.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.title
        book.title = request.POST['input']
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.TITLE,
            old_value=old_value,
            new_value=book.title
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
            'input_type': 'text',
            'page_number': book.title_page.number,
        }
        return render(request, f'lsma/edit/single-input.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.subtitle
        book.subtitle = request.POST['input']
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.SUBTITLE,
            old_value=old_value,
            new_value=book.subtitle
        )
        return redirect('/edit/subtitle')


class EditNumbersOffsetView(TemplateView):
    def get(self, request):
        book = Book.objects.exclude(checks__kind=BookCheck.Kind.NUMBERS_OFFSET).first()
        if book == None:
            return redirect('/')
        num_pages = book.pages.count()
        page = book.pages.all()[num_pages//2]
        context = {
            'page_title': 'Numbers Offset',
            'heading': 'Enter Numbers Offset',
            'image_url': page.jpg_image.url,
            'post_url': '/edit/numbers-offset',
            'label': 'Numbers Offset',
            'book_uuid': book.uuid,
            'previous_value': book.numbers_offset,
            'input_type': 'number',
            'page_number': page.number,
        }
        return render(request, f'lsma/edit/single-input.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.numbers_offset
        pdf_number = request.POST['page_number']
        book_number = request.POST['input']
        book.numbers_offset = int(pdf_number) - int(book_number)
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.NUMBERS_OFFSET,
            old_value=old_value,
            new_value=book.numbers_offset
        )
        if book.numbers_offset < 5 and book.roman_numbers_offset is None:
            BookCheck.objects.create(
                book=book,
                user=request.user,
                kind=BookCheck.Kind.ROMAN_NUMBERS_OFFSET,
                old_value=None,
                new_value=None,
            )
        return redirect('/edit/numbers-offset')


class EditRomanNumbersOffsetView(TemplateView):
    def get(self, request):
        book = Book.objects.exclude(checks__kind=BookCheck.Kind.ROMAN_NUMBERS_OFFSET).filter(numbers_offset__isnull=False).first()
        if book == None:
            return redirect('/')
        page = book.pages.all()[book.numbers_offset-3]
        context = {
            'page_title': 'Roman Numbers Offset',
            'heading': 'Enter Roman Numbers Offset',
            'image_url': page.jpg_image.url,
            'post_url': '/edit/roman-numbers-offset',
            'label': 'Roman Numbers Offset',
            'book_uuid': book.uuid,
            'previous_value': book.roman_numbers_offset,
            'input_type': 'number',
            'page_number': page.number,
        }
        return render(request, f'lsma/edit/single-input.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.roman_numbers_offset
        if request.POST['input']:
            pdf_number = request.POST['page_number']
            book_number = request.POST['input']
            book.roman_numbers_offset = int(pdf_number) - int(book_number)
        else:
            book.roman_numbers_offset = None
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.ROMAN_NUMBERS_OFFSET,
            old_value=old_value,
            new_value=book.roman_numbers_offset
        )
        return redirect('/edit/roman-numbers-offset')


class EditVolumeNumberView(TemplateView):
    def get(self, request):
        book = Book.objects.exclude(checks__kind=BookCheck.Kind.VOLUME_NUMBER).filter(title_page__isnull=False).first()
        if book == None:
            return redirect('/')
        context = {
            'page_title': 'Volume Number',
            'heading': 'Enter Volume Number',
            'image_url': book.title_page.jpg_image.url,
            'post_url': '/edit/volume-number',
            'label': 'Volume Number',
            'book_uuid': book.uuid,
            'previous_value': book.volume_number,
            'input_type': 'number',
            'page_number': book.title_page.number,
        }
        return render(request, f'lsma/edit/single-input.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.volume_number
        if request.POST['input']:
            book.volume_number = request.POST['input']
        else:
            book.volume_number = None
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.VOLUME_NUMBER,
            old_value=old_value,
            new_value=book.volume_number
        )
        return redirect('/edit/volume-number')


class EditEditionNumberView(TemplateView):
    def get(self, request):
        book = Book.objects.exclude(checks__kind=BookCheck.Kind.EDITION_NUMBER).filter(title_page__isnull=False).first()
        if book == None:
            return redirect('/')
        context = {
            'page_title': 'Edition Number',
            'heading': 'Enter Edition Number',
            'image_url': book.title_page.jpg_image.url,
            'post_url': '/edit/edition-number',
            'label': 'Edition Number',
            'book_uuid': book.uuid,
            'previous_value': book.edition_number,
            'input_type': 'number',
            'page_number': book.title_page.number,
        }
        return render(request, f'lsma/edit/single-input.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.edition_number
        if request.POST['input']:
            book.edition_number = request.POST['input']
        else:
            book.edition_number = None
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.EDITION_NUMBER,
            old_value=old_value,
            new_value=book.edition_number
        )
        return redirect('/edit/edition-number')


class EditIssueNumberView(TemplateView):
    def get(self, request):
        book = Book.objects.exclude(checks__kind=BookCheck.Kind.ISSUE_NUMBER).filter(title_page__isnull=False).first()
        if book == None:
            return redirect('/')
        context = {
            'page_title': 'Issue Number',
            'heading': 'Enter Issue Number',
            'image_url': book.title_page.jpg_image.url,
            'post_url': '/edit/issue-number',
            'label': 'Issue Number',
            'book_uuid': book.uuid,
            'previous_value': book.issue_number,
            'input_type': 'number',
            'page_number': book.title_page.number,
        }
        return render(request, f'lsma/edit/single-input.html', context=context)

    def post(self, request, *args, **kwargs):
        book = Book.objects.get(uuid=request.POST['book_uuid'])
        old_value = book.issue_number
        if request.POST['input']:
            book.issue_number = request.POST['input']
        else:
            book.issue_number = None
        book.save()
        BookCheck.objects.create(
            book=book,
            user=request.user,
            kind=BookCheck.Kind.ISSUE_NUMBER,
            old_value=old_value,
            new_value=book.issue_number
        )
        return redirect('/edit/issue-number')