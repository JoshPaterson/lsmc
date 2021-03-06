# Generated by Django 4.0.3 on 2022-04-19 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0025_alter_section_kind_sectioncheck'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graphiccheck',
            old_name='book',
            new_name='graphic',
        ),
        migrations.RenameField(
            model_name='sectioncheck',
            old_name='book',
            new_name='section',
        ),
        migrations.AlterField(
            model_name='bookcheck',
            name='kind',
            field=models.CharField(choices=[('SCA', 'Scan Color'), ('VEC', 'Has Vector Text'), ('TIP', 'Title Page'), ('TIT', 'Title'), ('SUB', 'Subtitle'), ('CON', 'Contributions'), ('VOL', 'Volume Number'), ('EDI', 'Edition Number'), ('ISS', 'Issue Number'), ('SER', 'Series'), ('CIT', 'Cities'), ('PUF', 'Publishing Frequency'), ('COP', 'Copyright Page'), ('DAT', 'Date Published'), ('INC', 'In Copyright'), ('COY', 'Copyright Years'), ('LIG', 'Has Ligatures'), ('PUB', 'Publishers'), ('PRN', 'Printing Number'), ('PIP', 'Printing Info Page'), ('PRI', 'Printers'), ('TOP', 'Topics'), ('SEC', 'Sections'), ('GRA', 'Graphics'), ('NUM', 'Numbers Offset'), ('RNO', 'Roman Numbers Offset'), ('LAN', 'Other Languages')], max_length=3),
        ),
    ]
