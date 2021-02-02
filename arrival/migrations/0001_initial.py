# Generated by Django 3.1.5 on 2021-01-19 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('office', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Arrival',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField(verbose_name='time delivered')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='office.customer')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='arrival.material')),
            ],
        ),
    ]
