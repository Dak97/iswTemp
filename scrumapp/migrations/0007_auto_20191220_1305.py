# Generated by Django 2.2.7 on 2019-12-20 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumapp', '0006_auto_20191220_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='description',
            field=models.TextField(default='Scrivi qui il testo', max_length=300, verbose_name='descrizione'),
        ),
    ]