# Generated by Django 3.1.6 on 2021-02-19 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0018_auto_20210219_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
