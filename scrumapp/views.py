from django.shortcuts import render, redirect, get_object_or_404
from scrumapp.models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login,
)
from scrumapp.models import Card
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

User = get_user_model()


def signup_view(request):
    title = 'Registrazione'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            card = Card.objects.all()
            for c in card:
                form.instance.user_card.add(c.id)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form, 'title': title})

# vista per la dashboard, un utente può entrare solo se loggato


class DashboardView(ListView):
    model = Board
    context_object_name = 'board_list'
    template_name = 'dashboard.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            id_current_user = self.request.user.id
            return Board.objects.filter(id_user=id_current_user)
        else:
            return Board.objects.none()

# vista per la creazione di una nuova board


class NewBoardView(CreateView):
    model = Board
    fields = ['name']
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.save()
        form.instance.id_user.set([self.request.user.id])
        return super(NewBoardView, self).form_valid(form)

    def get_success_url(self):
        return reverse('board', args=(self.object.id,))

# vista per la visualizzazione di una board


class BoardDetailView(DetailView):
    model = Board
    template_name = 'board.html'

    def get_context_data(self, **kwargs):
        context = super(BoardDetailView, self).get_context_data(**kwargs)
        id_b = self.object.id
        id_u = self.request.user.id
        context['column_list'] = Column.objects.filter(id_board=id_b)
        context['card_list'] = Card.objects.filter(id_user_card=id_u)
        return context

# vista per la creazione di una nuova colonna


class NewColumnView(CreateView):
    model = Column
    fields = ['name', 'id_board']
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_board.id,))

    def get_form(self, form_class=None):
        id_current_user = self.request.user.id
        form = super(NewColumnView, self).get_form(form_class)
        form.fields['id_board'].queryset = Board.objects.filter(id_user=id_current_user)
        return form

# vista per l eliminazione di una colonna


class DeleteColumnView(DeleteView):
    model = Column
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_board.id,))

# vista per la visualizzazione dei dettagli di una colonna


def modify_column_view(request, pk):
    column = get_object_or_404(Column, pk=pk)
    column_exclude_card_list = []
    id_u = request.user.id
    card_list = Card.objects.filter(id_column=pk).filter(id_user_card=id_u)
    exclude_card_list = Card.objects.exclude(id_column=pk).filter(id_user_card=id_u)
    for card in exclude_card_list:
        column_exclude_card_list.append(card.id_column)
    column_exclude_card_list = list(set(column_exclude_card_list))
    return render(request, 'modify_column.html', {'card_list': card_list, 'current_column': column,
                                                  'exclude_card_list': exclude_card_list,
                                                  'column_exclude_card_list': column_exclude_card_list})

# vista per la modifica di una colonna


class UpdateColumn(UpdateView):
    model = Column
    fields = ['name']
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_board.id,))

# vista per la creazione di una nuova card


class NewCardView(CreateView):
    model = Card
    fields = ['title', 'description', 'expiration_date', 'id_column']
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('board', args=(self.object.id_column.id_board.id,))

    def get_form(self, form_class=None):
        id_b = Board.objects.get(id=self.kwargs['pk'])
        form = super(NewCardView, self).get_form(form_class)
        form.fields['id_column'].queryset = Column.objects.filter(id_board=id_b)
        return form

    def form_valid(self, form):
        form.instance.save()
        user = User.objects.all()
        for u in user:
            form.instance.id_user_card.add(u.id)
        return super(NewCardView, self).form_valid(form)

# vista per la visualizzazione dei dettagli di una card


def modify_card_view(request, pk):
    card = get_object_or_404(Card, pk=pk)
    id_u = request.user.id
    user_list = User.objects.filter(user_card=pk).exclude(id=id_u)
    exclude_user_list = User.objects.exclude(user_card=pk)
    return render(request, 'modify_card.html', {'card': card, 'user_list': user_list,
                                                'exclude_user_list': exclude_user_list})

# vista per la modifica di una card


class UpdateCard(UpdateView):
    model = Card
    fields = ['title', 'description', 'expiration_date']
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('modify_card', args=(self.object.id,))

# vista per la modifica degli story points di una card


class UpdateCardSP(UpdateView):
    model = Card
    fields = ['story_points']
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('modify_card', args=(self.object.id,))

# vista per l eliminazione di un utente da una card, l'utente non potrà più vedere la card


def delete_user_from_card_view(request, pk, id_c):
    current_user = User.objects.get(id=pk)
    delete = 'eliminare'
    if request.method == 'POST':
        card = Card.objects.get(id=id_c)
        current_user.user_card.remove(card)
        return redirect('modify_card', pk=id_c)
    return render(request, 'confirm.html', {'current_user': current_user, 'value': delete})

# vista per l aggiunta di un utente a una card


def add_user_to_card(request, pk, id_c):
    current_user = User.objects.get(id=pk)
    add = 'aggiungere'
    if request.method == 'POST':
        card = Card.objects.get(id=id_c)
        current_user.user_card.add(card)
        return redirect('modify_card', pk=id_c)
    return render(request, 'confirm.html', {'current_user': current_user, 'value': add})

# vista per l eliminazione di una card


class DeleteCard(DeleteView):
    model = Card
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        return reverse('modify_column', args=(self.object.id_column.id,))

# vista per la modifica della colonna di appartenenza di una card


class UpdateIdColumn(UpdateView):
    model = Card
    fields = ['id_column']
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('modify_card', args=(self.object.id,))

# vista per spostare una card a un altra colonna


def add_card_to_column(request, pk, id_c):
    card = Card.objects.get(id=pk)
    add = 'aggiungere'
    if request.method == 'POST':
        card.id_column = Column.objects.get(id=id_c)
        card.save()
        return redirect('modify_column', pk=id_c)
    return render(request, 'confirm.html', {'card': card, 'value': add})

# vista per la visualizzazione dei dettagli degli utenti di una board


class ModifyIdUser(DetailView):
    model = Board
    template_name = 'modify_user.html'

    def get_context_data(self, **kwargs):
        id_u = self.request.user.id
        context = super(ModifyIdUser, self).get_context_data(**kwargs)
        id_b = self.object.id
        context['user_list'] = User.objects.filter(user_board=id_b)
        context['exclude_user_list'] = User.objects.exclude(user_board=id_b)
        context['delete_user_list'] = User.objects.filter(user_board=id_b).exclude(id=id_u)
        return context

# vista per la conferma di eliminazione di un utente da una board


def user_confirm_delete_view(request, pk, id_b):
    current_user = get_object_or_404(User, pk=pk)
    delete = 'eliminare'
    if request.method == 'POST':
        board = Board.objects.get(id=id_b)
        board.id_user.remove(current_user)
        return redirect('board', pk=id_b)
    return render(request, 'confirm.html', {'current_user': current_user, 'value': delete})

# vista per la conferma di aggiunta di un utente alla board


def add_user_confirm(request, pk, id_b):
    current_user = get_object_or_404(User, pk=pk)
    add = 'aggiungere'
    if request.method == 'POST':
        board = Board.objects.get(id=id_b)
        board.id_user.add(current_user)
        return redirect('board', pk=id_b)
    return render(request, 'confirm.html', {'current_user': current_user, 'value': add})

# vista per la bourndown


def burndown(request, pk):
    #board = Board.objects.get(id=pk)
    id_u = request.user.id
    #id_b = board.id
    card_dictionary = {}
    count_total_card = 0
    expired_card_counting = 0
    count_story_points = 0
    column_list = Column.objects.filter(id_board=pk)
    card_list = Card.objects.filter(id_user_card=id_u)
    for column in column_list:
        count_card = 0
        for card in card_list:
            if card.id_column.id == column.id:
                count_card += 1
                count_story_points = count_story_points + card.story_points
                if card.expiration_date < date.today():
                    expired_card_counting += 1
        card_dictionary.update({column.name: count_card})
        count_total_card = count_total_card + count_card
    return render(request, 'burndown.html', {'total_card': count_total_card,
                                             'card_dictionary': card_dictionary,
                                             'expired_card_counting': expired_card_counting,
                                             'story_points': count_story_points
                                             })
