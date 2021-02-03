# Generated by Django 3.1.6 on 2021-02-03 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arrival', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrival',
            name='arrival_time',
        ),
        migrations.AddField(
            model_name='arrival',
            name='arrived_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrival',
            name='gross_weight_kg',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrival',
            name='net_weight_kg',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrival',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Paid', 'Paid')], default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrival',
            name='tare_kg',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrival',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='office.scrappyuser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='material',
            name='price_per_kg',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='arrival',
            table='arrival',
        ),
        migrations.AlterModelTable(
            name='material',
            table='material',
        ),
    ]
