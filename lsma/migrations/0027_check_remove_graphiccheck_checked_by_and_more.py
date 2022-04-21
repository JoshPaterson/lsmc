# Generated by Django 4.0.3 on 2022-04-20 00:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lsma', '0026_rename_book_graphiccheck_graphic_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[('SCA', 'Scan Color'), ('VEC', 'Has Vector Text'), ('TIP', 'Title Page'), ('BTI', 'Book Title'), ('SUB', 'Subtitle'), ('BCO', 'Book Contributions'), ('VOL', 'Volume Number'), ('EDI', 'Edition Number'), ('ISS', 'Issue Number'), ('SER', 'Series'), ('CIT', 'Cities'), ('PUF', 'Publishing Frequency'), ('COP', 'Copyright Page'), ('DAT', 'Date Published'), ('INC', 'In Copyright'), ('COY', 'Copyright Years'), ('LIG', 'Has Ligatures'), ('PUB', 'Publishers'), ('PRN', 'Printing Number'), ('PIP', 'Printing Info Page'), ('PRI', 'Printers'), ('BTO', 'Book Topics'), ('SEC', 'Sections'), ('GRA', 'Graphics'), ('NUM', 'Numbers Offset'), ('RNO', 'Roman Numbers Offset'), ('LAN', 'Other Languages'), ('SKI', 'Section Kind'), ('KIB', 'Kind In Book'), ('STI', 'Section Title'), ('SNU', 'Section Number'), ('FED', 'For Edition'), ('FPA', 'First Page'), ('LPA', 'Last Page'), ('SCO', 'Section Contributions'), ('STO', 'Section Topics'), ('MED', 'Medium'), ('CON', 'Content'), ('COL', 'Print Color'), ('PAG', 'Pages'), ('ART', 'Artists'), ('CAP', 'Caption'), ('GTI', 'Graphic Title'), ('BOX', 'Box'), ('BWT', 'Box With Text'), ('GKI', 'Graphic Kind'), ('GNU', 'Graphic Number')], max_length=3)),
                ('checked', models.DateTimeField(blank=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='graphiccheck',
            name='checked_by',
        ),
        migrations.RemoveField(
            model_name='graphiccheck',
            name='graphic',
        ),
        migrations.RemoveField(
            model_name='sectioncheck',
            name='checked_by',
        ),
        migrations.RemoveField(
            model_name='sectioncheck',
            name='section',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='contributions',
            new_name='book_contributions',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='title',
            new_name='book_title',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='topics',
            new_name='book_topics',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='section_kind',
            new_name='graphic_kind',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='section_number',
            new_name='graphic_number',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='section_number_kind',
            new_name='graphic_number_kind',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='title',
            new_name='graphic_title',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='contributions',
            new_name='section_contributions',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='kind_in_book',
            new_name='section_kind_in_book',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='number',
            new_name='section_number',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='number_kind',
            new_name='section_number_kind',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='title',
            new_name='section_title',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='topics',
            new_name='section_topics',
        ),
        migrations.RemoveField(
            model_name='graphic',
            name='book',
        ),
        migrations.RemoveField(
            model_name='graphic',
            name='pages_checked',
        ),
        migrations.RemoveField(
            model_name='page',
            name='graphics',
        ),
        migrations.RemoveField(
            model_name='section',
            name='contributions_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='first_page_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='for_edition_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='kind',
        ),
        migrations.RemoveField(
            model_name='section',
            name='kind_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='kind_in_book_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='last_page_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='number_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='title_checked',
        ),
        migrations.RemoveField(
            model_name='section',
            name='topics_checked',
        ),
        migrations.AddField(
            model_name='box',
            name='empty',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='graphic',
            name='page',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='graphics', to='lsma.page'),
        ),
        migrations.AddField(
            model_name='section',
            name='section_kind',
            field=models.CharField(blank=True, choices=[('FMA', 'Front Matter'), ('BOD', 'Body'), ('BMA', 'Back Matter'), ('CHA', 'Chapter'), ('CHG', 'Chapter Group'), ('SUB', 'Subchapter'), ('PRE', 'Preface'), ('INT', 'Introduction'), ('DED', 'Dedication'), ('ACK', 'Acknowledgements'), ('TOC', 'Table Of Contents'), ('BIB', 'Bibliography'), ('GLO', 'Glossary'), ('APS', 'Appendices'), ('APP', 'Appendix'), ('IND', 'Index'), ('CAT', 'Publishers Catalog'), ('TAB', 'Table'), ('TAS', 'Tables'), ('ART', 'Article'), ('FIG', 'Figure'), ('PLA', 'Plates'), ('ERR', 'Errata'), ('OTH', 'Other')], max_length=3),
        ),
        migrations.DeleteModel(
            name='BookCheck',
        ),
        migrations.DeleteModel(
            name='GraphicCheck',
        ),
        migrations.DeleteModel(
            name='SectionCheck',
        ),
        migrations.AddField(
            model_name='check',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='lsma.book'),
        ),
        migrations.AddField(
            model_name='check',
            name='checked_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='check',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]