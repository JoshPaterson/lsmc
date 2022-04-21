# Generated by Django 4.0.3 on 2022-04-20 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lsma', '0030_rename_edited_by_edit_created_by_remove_edit_edited'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[('SCA', 'Scan Color'), ('VEC', 'Has Vector Text'), ('TIP', 'Title Page'), ('TIT', 'Title'), ('SUB', 'Subtitle'), ('CON', 'Contributions'), ('VOL', 'Volume Number'), ('EDI', 'Edition Number'), ('ISS', 'Issue Number'), ('SER', 'Series'), ('CIT', 'Cities'), ('PUF', 'Publishing Frequency'), ('COP', 'Copyright Page'), ('DAT', 'Date Published'), ('INC', 'In Copyright'), ('COY', 'Copyright Years'), ('LIG', 'Has Ligatures'), ('PUB', 'Publishers'), ('PRN', 'Printing Number'), ('PIP', 'Printing Info Page'), ('PRI', 'Printers'), ('TOP', 'Topics'), ('SEC', 'Sections'), ('GRA', 'Graphics'), ('NUM', 'Numbers Offset'), ('RNO', 'Roman Numbers Offset'), ('LAN', 'Other Languages')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='GraphicCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[('MED', 'Medium'), ('CON', 'Content'), ('COL', 'Print Color'), ('PAG', 'Pages'), ('ART', 'Artists'), ('CAP', 'Caption'), ('TIT', 'Title'), ('BOX', 'Box'), ('BWT', 'Box With Text'), ('KIN', 'Kind'), ('NUM', 'Number')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='SectionCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(choices=[('KIN', 'Kind'), ('KIB', 'Kind In Book'), ('TIT', 'Title'), ('NUM', 'Number'), ('FED', 'For Edition'), ('FPA', 'First Page'), ('LPA', 'Last Page'), ('CON', 'Contributions'), ('TOP', 'Topics')], max_length=3)),
            ],
        ),
        migrations.RenameField(
            model_name='book',
            old_name='book_contributions',
            new_name='contributions',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='book_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='book_topics',
            new_name='topics',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='graphic_kind',
            new_name='kind',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='graphic_number',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='graphic_number_kind',
            new_name='number_kind',
        ),
        migrations.RenameField(
            model_name='graphic',
            old_name='graphic_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_contributions',
            new_name='contributions',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_kind',
            new_name='kind',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_kind_in_book',
            new_name='kind_in_book',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_number',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_number_kind',
            new_name='number_kind',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_topics',
            new_name='topics',
        ),
        migrations.DeleteModel(
            name='Edit',
        ),
        migrations.AddField(
            model_name='sectioncheck',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='lsma.section'),
        ),
        migrations.AddField(
            model_name='sectioncheck',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='graphiccheck',
            name='graphic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='lsma.graphic'),
        ),
        migrations.AddField(
            model_name='graphiccheck',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookcheck',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checks', to='lsma.book'),
        ),
        migrations.AddField(
            model_name='bookcheck',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]