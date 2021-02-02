# Generated by Django 3.1.5 on 2021-01-27 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='', max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AddField(
            model_name='customer',
            name='surname',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='customer',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
