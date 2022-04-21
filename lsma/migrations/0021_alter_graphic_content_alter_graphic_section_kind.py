# Generated by Django 4.0.3 on 2022-04-16 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0020_remove_book_issue_number_kind_checked_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphic',
            name='content',
            field=models.CharField(blank=True, choices=[('PHO', 'Photograph'), ('MAP', 'Map'), ('CHA', 'Chart'), ('DIA', 'Diagram'), ('ILL', 'Illustration'), ('TEC', 'Technical Drawing'), ('DRA', 'Drawing'), ('DEC', 'Decoration'), ('EQU', 'Equation'), ('MUS', 'Music Notation'), ('TAB', 'Table')], max_length=3),
        ),
        migrations.AlterField(
            model_name='graphic',
            name='section_kind',
            field=models.CharField(blank=True, choices=[('FIG', 'Figure'), ('PLA', 'Plate'), ('EQU', 'Equation'), ('TAB', 'Table')], max_length=3),
        ),
    ]