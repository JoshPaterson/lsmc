# Generated by Django 4.0.3 on 2022-04-20 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lsma', '0028_remove_check_book_alter_check_kind'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[('SCA', 'Scan Color'), ('VEC', 'Has Vector Text'), ('TIP', 'Title Page'), ('BTI', 'Book Title'), ('SUB', 'Subtitle'), ('BCO', 'Book Contributions'), ('VOL', 'Volume Number'), ('EDI', 'Edition Number'), ('ISS', 'Issue Number'), ('SER', 'Series'), ('CIT', 'Cities'), ('PUF', 'Publishing Frequency'), ('COP', 'Copyright Page'), ('DAT', 'Date Published'), ('INC', 'In Copyright'), ('COY', 'Copyright Years'), ('LIG', 'Has Ligatures'), ('PUB', 'Publishers'), ('PRN', 'Printing Number'), ('PIP', 'Printing Info Page'), ('PRI', 'Printers'), ('BTO', 'Book Topics'), ('SEC', 'Sections'), ('GRA', 'Graphics'), ('NUM', 'Numbers Offset'), ('RNO', 'Roman Numbers Offset'), ('LAN', 'Other Languages'), ('SKI', 'Section Kind'), ('KIB', 'Section Kind In Book'), ('STI', 'Section Title'), ('SNU', 'Section Number'), ('FED', 'For Edition'), ('FPA', 'First Page'), ('LPA', 'Last Page'), ('SCO', 'Section Contributions'), ('STO', 'Section Topics'), ('MED', 'Medium'), ('CON', 'Content'), ('COL', 'Print Color'), ('PAG', 'Pages'), ('ART', 'Artists'), ('CAP', 'Caption'), ('GTI', 'Graphic Title'), ('BOX', 'Box'), ('BWT', 'Box With Text'), ('GKI', 'Graphic Kind'), ('GNU', 'Graphic Number')], max_length=3)),
                ('edited', models.DateTimeField(blank=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('edited_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Check',
        ),
    ]