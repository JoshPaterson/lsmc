# Generated by Django 4.0.3 on 2022-04-09 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0006_remove_box_page_original_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='height',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='page',
            name='width',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='original_image',
            field=models.ImageField(height_field='height', unique=True, upload_to='', width_field='width'),
        ),
    ]
