from django.test import TestCase, Client
from scrumapp.views import *
# Create your tests here.


class BaseTestView(TestCase):
    @classmethod
    def setUpClass(cls):
        super(BaseTestView, cls).setUpClass()
        cls.client = Client()
        cls.unlogged_client = Client()
        cls.user = User.objects.create_user(username='new_user')
        cls.user.set_password('new_password')
        cls.user.save()
        cls.another_user = User.objects.create_user(username='new_another_user')
        cls.another_user.set_password('new_another_password')
        cls.another_user.save()
        cls.board = Board.objects.create(name='board1')
        cls.board.id_user.set([cls.user])
        cls.another_board = Board.objects.create(name='another_board')
        cls.another_board.id_user.set([cls.another_user])
        cls.column = Column.objects.create(name='column1', id_board=cls.board)
        cls.another_column = Column.objects.create(name='another_column', id_board=cls.another_board)
        cls.card = Card.objects.create(
            title='card1', description='this is a new card', id_column=cls.column,
            expiration_date=date.today(), story_points=3
        )
        cls.card.id_user_card.set([cls.user])
        cls.another_card = Card.objects.create(
            title='another_card', description='this is an another card', id_column=cls.another_column,
            expiration_date=date.today(), story_points=3
        )
        cls.another_card.id_user_card.set([cls.another_user])

    def setUp(self):
        self.client.login(username='new_user', password='new_password')


class TestViews(BaseTestView):

    """def test_index(self):
        url = reverse('dashboard')
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.resolver_match.func, index)"""

    def test_dashboard(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, DashboardView.as_view().__name__)
        self.assertQuerysetEqual(
            response.context['board_list'], Board.objects.filter(id_user=self.user.id),
            transform=lambda x: x
        )
        self.assertFalse(response.context['board_list'] == Board.objects.exclude(id_user=self.user.id))
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_dashboard_false(self):
        response = self.unlogged_client.get('/')
        self.assertEqual(302, response.status_code)

    def test_new_board_view(self):
        response = self.client.get('/new_board/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, NewBoardView.as_view().__name__)
        self.assertTemplateUsed(response, 'form.html')
        form = {
            'name': 'new_board_test',
            'id_user': self.user.id,
        }
        url = reverse('new_board')
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Board.objects.count(), 3)
        url = reverse('board', args=(Board.objects.last().id,))
        self.assertRedirects(response, url, 302, 200)

    def test_board_detail_view(self):
        response = self.client.get(self.board.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, BoardDetailView.as_view().__name__)
        self.assertQuerysetEqual(
            response.context['column_list'], Column.objects.filter(id_board=self.column.id),
            transform=lambda x: x)
        self.assertQuerysetEqual(
            response.context['card_list'], Card.objects.filter(id_user_card=self.card.id),
            transform=lambda x: x)
        self.assertFalse(response.context['column_list'] ==
                         Column.objects.filter(id_board=self.another_column.id))
        self.assertFalse(response.context['card_list'] ==
                         Card.objects.filter(id_user_card=self.another_card.id))
        self.assertTemplateUsed(response, 'board.html')

    def test_new_column_view(self):
        response = self.client.get('/new_column/')
        self.assertEqual(response.status_code, 200)
        print(response.status_code)
        self.assertEqual(response.resolver_match.func.__name__, NewColumnView.as_view().__name__)
        self.assertTemplateUsed(response, 'form.html')
        form = {
            'name': 'new_column_test',
            'id_board': self.board.id,
        }
        url = reverse('new_column')
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Column.objects.count(), 3)
        url = reverse('board', args=(self.board.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_delete_column_view(self):
        url = reverse('delete_column', args=(self.column.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, DeleteColumnView.as_view().__name__)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertContains(response, 'Sei sicuro di voler eliminare')
        url = reverse('delete_column', args=(self.column.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Column.objects.count(), 1)
        url = reverse('board', args=(self.board.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_modify_column_view(self):
        url = reverse('modify_column', args=(self.column.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, modify_column_view)
        self.assertTemplateUsed(response, 'modify_column.html')
        self.assertQuerysetEqual(
            response.context['card_list'], Card.objects.filter(id_user_card=self.user.id),
            transform=lambda x: x
        )
        self.assertTrue(response.context['current_column'], self.column)

    def test_update_column_view(self):
        url = reverse('update_column', args=(self.column.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, UpdateColumn.as_view().__name__)
        self.assertTemplateUsed(response, 'form.html')
        url = reverse('update_column', args=(self.column.id,))
        form = {
            'name': 'new_column_test',
        }
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Column.objects.count(), 2)
        url = reverse('board', args=(self.board.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_new_card_view(self):
        url = reverse('new_card', args=(self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, NewCardView.as_view().__name__)
        self.assertTemplateUsed(response, 'form.html')
        form = {
            'title': 'new_card_test',
            'description': 'new_description_test',
            'expiration_date': date.today(),
            'id_column': self.column.id,
        }
        url = reverse('new_card', args=(self.card.id,))
        response = self.client.post(url, form)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 3)
        url = reverse('board', args=(self.board.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_modify_card_view(self):
        url = reverse('modify_card', args=(self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, modify_card_view)
        self.assertTemplateUsed(response, 'modify_card.html')
        self.assertQuerysetEqual(
            response.context['user_list'], User.objects.filter(user_card=self.card.id),
            transform=lambda x: x
        )
        self.assertQuerysetEqual(
            response.context['exclude_user_list'], User.objects.exclude(user_card=self.card.id),
            transform=lambda x: x
        )
        self.assertTrue(response.context['card'], self.card)

    def test_update_card_view(self):
        url = reverse('update_card', args=(self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, UpdateCard.as_view().__name__)
        self.assertTemplateUsed(response, 'form.html')
        url = reverse('update_card', args=(self.card.id,))
        form = {
            'title': 'new_card_test',
            'description': 'new_description_test',
            'expiration_date': date.today()
        }
        response = self.client.post(url, form)
        self.card.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.card.title, 'new_card_test')
        self.assertEqual(self.card.description, 'new_description_test')
        self.assertEqual(self.card.expiration_date, date.today())
        url = reverse('modify_card', args=(self.card.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_update_card_sp_view(self):
        url = reverse('update_sp_card', args=(self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, UpdateCardSP.as_view().__name__)
        self.assertTemplateUsed(response, 'form.html')
        url = reverse('update_sp_card', args=(self.card.id,))
        form = {
            'story_points': 4
        }
        response = self.client.post(url, form)
        self.card.refresh_from_db()
        self.assertEqual(self.card.story_points, 4)
        self.assertEqual(response.status_code, 302)
        url = reverse('modify_card', args=(self.card.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_delete_user_from_card_view(self):
        url = reverse('delete_user_from_card', args=(self.user.id, self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, delete_user_from_card_view)
        self.assertTemplateUsed(response, 'confirm.html')
        self.assertTrue(response.context['current_user'], self.user)
        self.assertTrue(response.context['value'], 'eliminare')
        url = reverse('delete_user_from_card', args=(self.user.id, self.card.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.card.id_user_card.count(), 0)
        url = reverse('modify_card', args=(self.card.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_add_user_to_card_view(self):
        url = reverse('add_user_to_card', args=(self.another_user.id, self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, add_user_to_card)
        self.assertTemplateUsed(response, 'confirm.html')
        self.assertTrue(response.context['current_user'], self.another_user)
        self.assertTrue(response.context['value'], 'aggiungere')
        url = reverse('add_user_to_card', args=(self.another_user.id, self.card.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.card.id_user_card.count(), 2)
        url = reverse('modify_card', args=(self.card.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_delete_card_view(self):
        url = reverse('delete_card', args=(self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, DeleteCard.as_view().__name__)
        self.assertTemplateUsed(response, 'confirm_delete.html')
        self.assertContains(response, 'Sei sicuro di voler eliminare')
        url = reverse('delete_card', args=(self.card.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 1)
        url = reverse('modify_column', args=(self.column.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_update_id_column_view(self):
        url = reverse('update_id_column', args=(self.card.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, UpdateIdColumn.as_view().__name__)
        self.assertTemplateUsed(response, 'form.html')
        url = reverse('update_id_column', args=(self.card.id,))
        form = {
            'id_column': self.another_column.id,
        }
        response = self.client.post(url, form)
        self.card.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.card.id_column.id, self.another_column.id)
        url = reverse('modify_card', args=(self.card.id,))
        self.assertRedirects(response, url, 302, 200)

    def add_card_to_column_view(self):
        url = reverse('add_card_to_column', args=(self.another_card.id, self.column.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, add_card_to_column)
        self.assertTemplateUsed(response, 'confirm.html')
        self.assertTrue(response.context['card'], self.another_card)
        self.assertTrue(response.context['value'], 'aggiungere')
        url = reverse('add_card_to_column', args=(self.another_card.id, self.column.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        #self.assertEqual(self.another_card.id_user_card.count(), 2)
        url = reverse('modify_card', args=(self.another_card.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_modify_id_user_view(self):
        url = reverse('new_user', args=(self.board.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, ModifyIdUser.as_view().__name__)
        self.assertQuerysetEqual(
            response.context['user_list'], User.objects.filter(user_board=self.board.id),
            transform=lambda x: x)
        self.assertFalse(response.context['user_list'] ==
                         User.objects.filter(user_board=self.another_board.id))
        self.assertTemplateUsed(response, 'modify_user.html')

    def test_user_confirm_delete_view(self):
        url = reverse('user_confirm_delete', args=(self.user.id, self.board.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, user_confirm_delete_view)
        self.assertTemplateUsed(response, 'confirm.html')
        self.assertTrue(response.context['current_user'], self.user)
        self.assertTrue(response.context['value'], 'eliminare')
        url = reverse('user_confirm_delete', args=(self.user.id, self.board.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.board.id_user.count(), 0)
        url = reverse('board', args=(self.board.id,))
        self.assertRedirects(response, url, 302, 200)

    """def test_user_delete_view(self):
        url = reverse('delete_user', args=(self.board.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, user_delete_view)
        self.assertQuerysetEqual(
            response.context['user_list'], User.objects.filter(user_board=self.board.id).exclude(id=self.user.id),
            transform=lambda x: x
        )
        self.assertFalse(response.context['user_list'] ==
                         User.objects.filter(user_board=self.board.id).filter(id=self.user.id))
        self.assertTemplateUsed(response, 'delete_user.html')"""

    """def test_add_user_view(self):
        url = reverse('add_user', args=(self.board.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, add_user_view)
        self.assertQuerysetEqual(
            response.context['user_list'], User.objects.exclude(user_board=self.board.id),
            transform=lambda x: x
        )
        self.assertEqual(response.context['b'], self.board)
        self.assertFalse(response.context['user_list'] == User.objects.filter(user_board=self.board.id))
        self.assertFalse(response.context['b'] == self.another_board)
        self.assertTemplateUsed(response, 'add_user.html')"""

    def test_add_user_confirm(self):
        url = reverse('add_user_confirm', args=(self.another_user.id, self.board.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, add_user_confirm)
        self.assertTemplateUsed(response, 'confirm.html')
        self.assertTrue(response.context['current_user'], self.user)
        self.assertTrue(response.context['value'], 'aggiungere')
        url = reverse('add_user_confirm', args=(self.another_user.id, self.board.id,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.board.id_user.count(), 2)
        url = reverse('board', args=(self.board.id,))
        self.assertRedirects(response, url, 302, 200)

    def test_burndown(self):
        count_total_card = 0
        count_card_scadute = 0
        count_story_points = 0
        card_dictionary = {}
        url = reverse('burndown', args=(self.board.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, burndown)
        self.assertTemplateUsed(response, 'burndown.html')
        column_list = Column.objects.filter(id_board=self.board.id)
        card_list = Card.objects.filter(id_user_card=self.user.id)
        for column in column_list:
            count_card = 0
            for card in card_list:
                if card.id_column.id == column.id:
                    count_card += 1
                    count_story_points = count_story_points + card.story_points
                    if card.expiration_date < date.today():
                        count_card_scadute += 1
            card_dictionary.update({column.name: count_card})
            count_total_card = count_total_card + count_card
        self.assertTrue(response.context['total_card'], count_total_card)
        self.assertTrue(response.context['card_dictionary'], card_dictionary)
        self.assertTrue(response.context['card_scadute'], count_card_scadute)
        self.assertTrue(response.context['story_points'], count_story_points)
