# Generated by Django 4.0.3 on 2022-04-12 00:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0010_alter_box_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='other_languages',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('FRE', 'French'), ('GER', 'German'), ('LAT', 'Latin'), ('GRE', 'Greek'), ('IND', 'Indonesian')], max_length=15), blank=True, null=True, size=None),
        ),
    ]