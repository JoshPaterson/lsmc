# Generated by Django 4.0.3 on 2022-04-09 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0004_alter_ocrfix_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='page_original_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
