from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
User = get_user_model()


def all_users():
    return User.objects.all()


class Board(models.Model):
    name = models.CharField(max_length=100)
    id_user = models.ManyToManyField(User, related_name='user_board')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('nuovo_utente', args=[str(self.id)])

    def get_pk(self):
        return reverse('board', args=[str(self.id)])

    def get_pk_new_user(self):
        return reverse('add_user', args=[str(self.id)])

    def get_pk_delete_user(self):
        return reverse('delete_user', args=[str(self.id)])

    def get_pk_confirm(self):
        return reverse('user_confirm_delete', args=[str(self.id)])

    def get_pk_burndown(self):
        return reverse('burndown', args=[str(self.id)])



class Column(models.Model):
    name = models.CharField(max_length=100)
    id_board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('UpdateColumn', args=[str(self.id)])

    def get_pk(self):
        return reverse('modify_column', args=[str(self.id)])

    def get_pk_delete(self):
        return reverse('delete_column', args=[str(self.id)])

    def get_pk_new(self):
        return reverse('NewCard', args=[str(self.id)])


class Card(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='Scrivi qui il testo')
    expiration_date = models.DateField(default=date.today)
    story_points = models.PositiveSmallIntegerField(default=0, help_text='inserisci un valore da 1 a 5',
                                                    validators=[
                                                        MinValueValidator(1), MaxValueValidator(5)
                                                    ])
    id_column = models.ForeignKey(Column, on_delete=models.CASCADE)
    id_user_card = models.ManyToManyField(User, related_name='user_card')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('DeleteCard', args=[str(self.id)])

    def get_pk_modify(self):
        return reverse('modify_card', args=[str(self.id)])

    def get_pk(self):
        return reverse('UpdateCard', args=[str(self.id)])

    def get_pk_sp(self):
        return reverse('UpdateCardSP', args=[str(self.id)])

    def get_pk_modify_column(self):
        return reverse('UpdateIdColumn', args=[str(self.id)])



    """def set_name(self, *args):
        nuova_board = Board.objects.create(name='')"""



"""class UtenteBoard(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    id_board = models.ForeignKey(Board, on_delete=models.CASCADE)"""






