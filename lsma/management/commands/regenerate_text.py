from django.core.management.base import BaseCommand, CommandError
from lsma.models import Page

class Command(BaseCommand):
    help = 'Regenerate text for all pages'

    def handle(self, *args, **options):
        for page in Page.objects.all():
            page.generate_text()