from django.test import TestCase
from ..store.forms import MyForm


class MyModelTest(TestCase):
    def setUp(self):
        self.obj = MyModel.objects.create(name='test', age=30)

    def test_my_model_name(self):
        self.assertEqual(self.obj.name, 'test')

    def test_my_model_age(self):
        self.assertEqual(self.obj.age, 30)
