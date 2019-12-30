from django.test import TestCase
from scrumapp.models import *
from datetime import date
# Create your tests here.


"""class ModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ModelTest, cls).setUpClass()
        new_user = get_user_model()
        cls.user = new_user.objects.create(username='new_user', password='new_password')
        cls.board = Board.objects.create(name="new_board")
        cls.board.id_user.set([cls.user])
        cls.board.save()
        cls.column = Column.objects.create(name='new_column', id_board=cls.board)
        cls.card = Card.objects.create(
            title='new_card', description='this is a new card', id_column=cls.column,
            expiration_date=date.today(), story_points=3
        )
        cls.card.id_user_card.set([cls.user])
        cls.card.save()


class ModelTestCase(ModelTest):
    def testFindModels(self):
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(len(Board.objects.all()), 1)
        self.assertEqual(len(Column.objects.all()), 1)
        self.assertEqual(len(Card.objects.all()), 1)
#   controllo che i dati siano giusti

    def testCorrectData(self):
        self.assertEquals(self.user.username, 'new_user')
        self.assertEquals(self.user.password, 'new_password')

        self.assertEquals(self.board.name, 'new_board')
        self.assertTrue(self.user in self.board.id_user.all())

        self.assertEquals(self.column.name, 'new_column')
        self.assertEquals(self.column.id_board, self.board)

        self.assertEquals(self.card.title, 'new_card')
        self.assertEquals(self.card.description, 'this is a new card')
        self.assertEquals(self.card.expiration_date, date.today())
        self.assertEquals(self.card.story_points, 3)
        self.assertEquals(self.card.id_column, self.column)
        self.assertTrue(self.user in self.card.id_user_card.all())
#   controllo che la dimensione sia quella giusta

    def testMaxLength(self):
        max_length_name_board = self.board._meta.get_field('name').max_length
        self.assertEquals(max_length_name_board, 100)

        max_length_name_column = self.column._meta.get_field('name').max_length
        self.assertEquals(max_length_name_column, 100)

        max_length_name_card = self.card._meta.get_field('title').max_length
        self.assertEquals(max_length_name_card, 100)
#   controllo che le funzioni restituiscano dati corretti

    def testGetAbsoluteUrl(self):
        self.assertEquals(self.board.get_absolute_url(), '/board/1')

    def testStr(self):
        self.assertEquals(self.board.__str__(), 'new_board')

        self.assertEquals(self.column.__str__(), 'new_column')

        self.assertEquals(self.card.__str__(), 'new_card: this is a new card')"""
