# Generated by Django 4.0.3 on 2022-04-09 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0002_remove_page_jpg_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='text_direction',
            new_name='text_top_rotated_to',
        ),
    ]