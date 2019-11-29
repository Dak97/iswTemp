from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Board, Column, Card
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.utils.translation import gettext_lazy as _
from .models import Column as ColumnModel
from .models import Card as CardModel
import datetime

# Create your views here.

User = get_user_model()


def index(request):
    return render(
        request,
        'index.html', {'username': User.username}
    )


class dashboard_view(ListView):
    model = Board
    context_object_name = 'board_list'
    template_name = 'dashboard.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            id_utente = self.request.user.id
            return Board.objects.filter(id_user=id_utente)
        else:
            return Board.objects.none()


    """def dashboard_view(request):
    id_utente = request.user.id
    all_board = Board.objects.filter(id_user=id_utente)
    return render(request, 'dashboard.html', {'board_list': all_board})"""


class nuova_board_view(CreateView):
    model = Board
    fields = ['name']
    template_name = 'board_form.html'
    #context_object_name = 'board_list'
    #queryset = Board.objects.all()

    def form_valid(self, form):
        form.instance.save()
        form.instance.id_user.set([self.request.user.id])
        return super(nuova_board_view, self).form_valid(form)

    def get_success_url(self):
        return reverse('board', args=(self.object.id,))


class board_view(DetailView):
    model = Board
    template_name = 'board.html'

    def get_context_data(self, **kwargs):
        context = super(board_view, self).get_context_data(**kwargs)
        id_b = self.object.id
        id_u = self.request.user.id
        context['column_list'] = Column.objects.filter(id_board=id_b)
        #context['card_list'] = Card.objects.all()
        context['card_list'] = Card.objects.filter(id_user_card=id_u)
        return context

    """@model
    def get_absolute_url(self):
        return reverse('aggiungi_utente_view', args=[str(self.id)])"""


"""class aggiungi_utente_view(UpdateView):
    model = Board
    fields = ['id_user']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id,))

    def get_form(self, form_class=None):
        id_b = self.object.id
        form = super(aggiungi_utente_view, self).get_form(form_class)
        form.fields['id_user'].label = "scegli l utente da aggiungere alla board"
        form.fields['id_user'].queryset = User.objects.exclude(user_board=id_b)
        return form"""


class nuova_colonna_view(CreateView):
    model = Column
    fields = ['name', 'id_board']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_board.id,))

    def get_form(self, form_class=None):
        id_utente = self.request.user.id
        form = super(nuova_colonna_view, self).get_form(form_class)
        form.fields['id_board'].queryset = Board.objects.filter(id_user=id_utente)
        return form


class delete_column(DeleteView):
    model = Column
    template_name = 'confirm_delete_column.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_board.id,))


def modify_column_view(request, pk):
    column = get_object_or_404(Column, pk=pk)
    id_u = request.user.id
    card_list = Card.objects.filter(id_column=pk).filter(id_user_card=id_u)
    return render(request, 'modify_column.html', {'card_list': card_list, 'col': column})


class UpdateColumn(UpdateView):
    model = Column
    fields = ['name']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_board.id,))


class nuova_card_view(CreateView):
    model = Card
    fields = ['title', 'description', 'expiration_date', 'id_column']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_column.id_board.id,))

    def form_valid(self, form):
        form.instance.save()
        user = User.objects.all()
        for u in user:
            form.instance.id_user_card.add(u.id)
        return super(nuova_card_view, self).form_valid(form)


def modify_card_view(request, pk):
    card = get_object_or_404(Card, pk=pk)
    user_list = User.objects.filter(user_card=pk)
    exclude_user_list = User.objects.exclude(user_card=pk)
    return render(request, 'modify_card.html', {'card': card, 'user_list': user_list,
                                                'exclude_user_list': exclude_user_list})


class UpdateCard(UpdateView):
    model = Card
    fields = ['title', 'description', 'expiration_date']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('modify_card', args=(self.object.id,))


class UpdateCardSP(UpdateView):
    model = Card
    fields = ['story_points']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('modify_card', args=(self.object.id,))


def delete_user_from_card_view(request, pk, id_c):
    utente = User.objects.get(id=pk)
    delete = 'eliminare'
    if request.method == 'POST':
        card = Card.objects.get(id=id_c)
        utente.user_card.remove(card)
        return redirect('modify_card', pk=id_c)
    return render(request, 'user_confirm.html', {'utente': utente, 'value': delete})


def add_user_to_card(request, pk, id_c):
    utente = User.objects.get(id=pk)
    add = 'aggiungere'
    if request.method == 'POST':
        card = Card.objects.get(id=id_c)
        card.id_user_card.add(utente)
        return redirect('modify_card', pk=id_c)
    return render(request, 'user_confirm.html', {'utente': utente, 'value': add})



class DeleteCard(DeleteView):
    model = Card
    template_name = 'confirm_delete_column.html'

    def get_success_url(self):
        return reverse('modify_column', args=(self.object.id_column.id,))


class UpdateIdColumn(UpdateView):
    model = Card
    fields = ['id_column']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('modify_card', args=(self.object.id,))


class NewCard(CreateView):
    model = Card
    fields = ['title', 'description', 'expiration_date']
    template_name = 'board_form.html'

    def get_success_url(self):
        return reverse('modify_column', args=(self.object.id_column.id,))

    def form_valid(self, form):
        form.instance.id_column = Column.objects.get(id=self.kwargs['pk'])
        form.instance.save()
        user = User.objects.all()
        for u in user:
            form.instance.id_user_card.add(u.id)
        return super(NewCard, self).form_valid(form)


class new_user_view(DetailView):
    model = Board
    template_name = 'new_user.html'

    def get_context_data(self, **kwargs):
        context = super(new_user_view, self).get_context_data(**kwargs)
        id_b = self.object.id
        context['user_list'] = User.objects.filter(user_board=id_b)
        return context


def user_confirm_delete_view(request, pk, id_b):
    utente = get_object_or_404(User, pk=pk)
    delete = 'eliminare'
    if request.method == 'POST':
        board = Board.objects.get(id=id_b)
        board.id_user.remove(utente)
        return redirect('board', pk=id_b)
    return render(request, 'user_confirm.html', {'utente': utente, 'value': delete})


def user_delete_view(request, pk):
    utente = request.user.id
    board = get_object_or_404(Board, pk=pk)
    lista_utenti = User.objects.filter(user_board=pk).exclude(id=utente)
    return render(request, 'delete_user.html', {'user_list': lista_utenti, 'b': board})


def add_user_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    lista_utenti = User.objects.exclude(user_board=pk)
    return render(request, 'add_user.html', {'user_list': lista_utenti, 'b': board})


def add_user_confirm(request, pk, id_b):
    utente = get_object_or_404(User, pk=pk)
    add = 'aggiungere'
    if request.method == 'POST':
        board = Board.objects.get(id=id_b)
        board.id_user.add(utente)
        return redirect('board', pk=id_b)
    return render(request, 'user_confirm.html', {'utente': utente, 'value': add})


def burndown(request, pk):
    board = Board.objects.get(id=pk)
    id_b = board.id
    card_dictionary = {}
    count_total_card = 0
    count_card_scadute = 0
    count_story_points = 0
    column_list = Column.objects.filter(id_board=id_b)
    card_list = Card.objects.all()
    for column in column_list:
        count_card = 0
        for card in card_list:
            if card.id_column.id == column.id:
                count_card += 1
                count_story_points = count_story_points + card.story_points
                if card.expiration_date < datetime.date.today():
                    count_card_scadute += 1
        card_dictionary.update({column.name: count_card})
        count_total_card = count_total_card + count_card
    return render(request, 'burndown.html', {
        'card_list': card_list, 'column_list': column_list, 'total_card': count_total_card,
        'card_dictionary': card_dictionary, 'card_scadute': count_card_scadute,
        'story_points': count_story_points})


"""def get_form(self, form_class=None):
        id_utente = self.request.user.id
        form = super(nuova_card_view, self).get_form(form_class)
        form.fields['id_column'].queryset = Board.objects.filter(id_user=id_utente)
        return form"""


"""def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(aggiungi_utente_view, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['board_list'] = Board.objects.all()
        return context
    def get_object(self):
        return get_object_or_404(Board, id=id)
        #pk=self.request.board.id)"""


"""def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(nuova_board_view, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['board_list'] = Board.objects.all()
        return context"""


"""def board_view(request):
    return render(
        request,
        'board.html'
    )"""
