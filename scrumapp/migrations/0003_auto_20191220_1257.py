# Generated by Django 2.2.7 on 2019-12-20 12:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumapp', '0002_auto_20191220_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='card',
            name='description',
            field=models.TextField(default='Scrivi qui il testo', verbose_name='descrizione'),
        ),
        migrations.AlterField(
            model_name='card',
            name='expiration_date',
            field=models.DateField(default=datetime.date.today, verbose_name='data di scadenza'),
        ),
        migrations.AlterField(
            model_name='column',
            name='name',
            field=models.CharField(max_length=100, verbose_name='nome'),
        ),
    ]
