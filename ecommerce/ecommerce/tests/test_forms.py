from django.test import TestCase
from django.contrib.auth.models import User
from store.forms import OrderForm, CreateUserForm


class TestOrderForm(TestCase):
    def test_order_form_valid_data(self):
        form = OrderForm(data={
            'customer_name': 'John Doe',
            'customer_email': 'johndoe@example.com',
            'product': 'Test product',
            'quantity': 2,
            'price': 10.99
        })

        self.assertTrue(form.is_valid())

    def test_order_form_no_data(self):
        form = OrderForm(data={})

        self.assertFalse(form.is_valid())
        # customer_name, customer_email, product, quantity are required
        self.assertEquals(len(form.errors), 4)


class TestCreateUserForm(TestCase):
    def test_create_user_form_valid_data(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123'
        })

        self.assertTrue(form.is_valid())

    def test_create_user_form_different_passwords(self):
        form = CreateUserForm(data={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'differentpass123'
        })

        self.assertFalse(form.is_valid())
        # password2 error message should be present
        self.assertIn('password2', form.errors)

    def test_create_user_form_existing_username(self):
        # create a user to test the case where the username already exists
        User.objects.create_user(
            username='existinguser', email='existinguser@example.com', password='existingpass')

        form = CreateUserForm(data={
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        })

        self.assertFalse(form.is_valid())
        # username error message should be present
        self.assertIn('username', form.errors)
