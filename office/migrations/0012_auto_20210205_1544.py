# Generated by Django 3.1.6 on 2021-02-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0011_auto_20210205_1415'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.RemoveField(
            model_name='customer',
            name='tax_id',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='vat_id',
        ),
        migrations.AddField(
            model_name='customer',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
    ]
