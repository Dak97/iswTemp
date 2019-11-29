# Generated by Django 2.2.7 on 2019-11-26 20:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scrumapp', '0016_auto_20191126_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='id_user_card',
            field=models.ManyToManyField(related_name='user_card', to=settings.AUTH_USER_MODEL),
        ),
    ]
