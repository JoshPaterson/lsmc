# Generated by Django 4.0.3 on 2022-04-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0021_alter_graphic_content_alter_graphic_section_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='graphic',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='graphic',
            name='title_checked',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]