from django.test import TestCase
from django.urls import reverse
from store.views import MyView


class MyViewTest(TestCase):
    def test_my_view(self):
        url = reverse('myview')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/myview.html')
