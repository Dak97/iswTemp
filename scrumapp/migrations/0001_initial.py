# Generated by Django 2.2.7 on 2019-11-29 15:40

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('id_user', models.ManyToManyField(related_name='user_board', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('id_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrumapp.Board')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default='Scrivi qui il testo')),
                ('expiration_date', models.DateField(default=datetime.date.today)),
                ('story_points', models.PositiveSmallIntegerField(default=0, help_text='inserisci un valore da 1 a 5', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('id_column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scrumapp.Column')),
                ('id_user_card', models.ManyToManyField(related_name='user_card', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
