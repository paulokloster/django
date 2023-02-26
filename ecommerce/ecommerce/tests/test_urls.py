from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import MyView


class MyUrlsTest(SimpleTestCase):
    def test_my_view_url(self):
        url = reverse('myview')
        self.assertEqual(resolve(url).func.view_class, MyView)
