# Generated by Django 2.2.7 on 2019-11-26 12:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumapp', '0014_auto_20191126_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='story_points',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]