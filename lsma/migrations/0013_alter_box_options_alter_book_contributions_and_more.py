# Generated by Django 4.0.3 on 2022-04-12 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lsma', '0012_alter_box_page'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='box',
            options={'ordering': ['order'], 'verbose_name_plural': 'boxes'},
        ),
        migrations.AlterField(
            model_name='book',
            name='contributions',
            field=models.ManyToManyField(blank=True, related_name='books', to='lsma.contribution'),
        ),
        migrations.AlterField(
            model_name='book',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='books', to='lsma.topic'),
        ),
        migrations.AlterField(
            model_name='graphic',
            name='artists',
            field=models.ManyToManyField(related_name='graphics', to='lsma.person'),
        ),
        migrations.AlterField(
            model_name='page',
            name='graphics',
            field=models.ManyToManyField(blank=True, related_name='pages', to='lsma.graphic'),
        ),
        migrations.AlterField(
            model_name='page',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='pages', to='lsma.topic'),
        ),
        migrations.AlterField(
            model_name='section',
            name='contributions',
            field=models.ManyToManyField(blank=True, related_name='sections', to='lsma.contribution'),
        ),
        migrations.AlterField(
            model_name='section',
            name='pages',
            field=models.ManyToManyField(blank=True, related_name='sections', to='lsma.page'),
        ),
        migrations.AlterField(
            model_name='section',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='sections', to='lsma.topic'),
        ),
        migrations.AlterField(
            model_name='table',
            name='heading_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_headings', to='lsma.page'),
        ),
        migrations.AlterField(
            model_name='table',
            name='topics',
            field=models.ManyToManyField(related_name='tables', to='lsma.topic'),
        ),
    ]
