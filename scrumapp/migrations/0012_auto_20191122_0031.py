# Generated by Django 2.2.7 on 2019-11-22 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumapp', '0011_auto_20191122_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='description',
            field=models.TextField(default='Scrivi qui il testo'),
        ),
    ]