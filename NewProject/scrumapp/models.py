from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

User = get_user_model()


class Board(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    id_user = models.ManyToManyField(User, related_name='user_board', verbose_name='utente')

    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board', args=[str(self.pk)])


class Column(models.Model):
    name = models.CharField(max_length=100, verbose_name='nome')
    id_board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='board')

    objects = models.Manager()

    def __str__(self):
        return self.name


class Card(models.Model):
    title = models.CharField(max_length=100, verbose_name='titolo')
    description = models.TextField(default='Scrivi qui il testo', max_length=300, verbose_name='descrizione')
    expiration_date = models.DateField(default=date.today, verbose_name='data di scadenza')
    story_points = models.PositiveSmallIntegerField(default=0, help_text='inserisci un valore da 1 a 5',
                                                    validators=[
                                                        MinValueValidator(1), MaxValueValidator(5)
                                                    ])
    id_column = models.ForeignKey(Column, on_delete=models.CASCADE, verbose_name='colonna')
    id_user_card = models.ManyToManyField(User, related_name='user_card', verbose_name='utente')

    objects = models.Manager()

    def __str__(self):
        return '{}: {}' .format(self.title, self.description)
