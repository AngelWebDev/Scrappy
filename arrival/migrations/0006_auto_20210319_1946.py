# Generated by Django 3.1.6 on 2021-03-19 19:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0020_auto_20210219_1745'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arrival', '0005_auto_20210319_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrival',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='office.customer'),
        ),
        migrations.AlterField(
            model_name='arrival',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='arrivalpos',
            name='arrival',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='arrival.arrival'),
        ),
        migrations.AlterField(
            model_name='arrivalpos',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='arrival.material'),
        ),
    ]
