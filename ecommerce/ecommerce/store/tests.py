from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestViews(TestCase):

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/home.html')

    def test_register_view_valid_data(self):
        url = reverse('register')
        response = self.client.post(url, {'username': 'testuser', 'email': 'testuser@example.com',
                                    'password1': 'testpass1234', 'password2': 'testpass1234'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'),
                             status_code=302, target_status_code=200)

    def test_register_view_invalid_data(self):
        url = reverse('register')
        response = self.client.post(url, {'username': 'testuser', 'email': 'testuser@example.com',
                                    'password1': 'testpass1234', 'password2': 'testpass1234'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'),
                             status_code=302, target_status_code=200)

    # def test_register_view_invalid_data(self):
    #     url = reverse('register')
    #     response = self.client.post(url, {'username': 'testuser', 'email': 'testuser@example.com',
    #                                 'password1': 'testpass1234', 'password2': 'testpass12345'})
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'store/register.html')
    #     self.assertContains(
    #         response, "The two password fields didn&#x27;t match.")

    def test_login_view_valid_credentials(self):
        User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass1234')
        url = reverse('login')
        response = self.client.post(
            url, {'username': 'testuser', 'password': 'testpass1234'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'home'), status_code=302, target_status_code=200)

    def test_login_view_invalid_credentials(self):
        url = reverse('login')
        response = self.client.post(
            url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/login.html')
        self.assertContains(response, "username OR password is incorrect")
