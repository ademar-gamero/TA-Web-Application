from django.test import TestCase
from django.urls import reverse
from ta_app.models import User

class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            password='testpassword123',
            email='test@example.com',
            name='Test User',
            role='TA'
        )
        self.login_url = reverse('login')
    def test_successful_login(self):
        response = self.client.post(self.login_url, {'username': 'testuser','password': 'testpassword123'}, follow=True)
        self.assertRedirects(response, reverse('Home'))
        self.assertTrue('role' in self.client.session and self.client.session['role'] == 'TA')
        self.assertTrue('name' in self.client.session and self.client.session['name'] == 'Test User')
        # Successful login test

    def test_incorrect_password(self):
        response = self.client.post(self.login_url, {'username': 'testuser','password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password.', response.content.decode())
        # Wrong password test

    def test_empty_username(self):
        response = self.client.post(self.login_url, {'username': '','password': 'testpassword123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter your username.', response.content.decode())
        # Empty username test

    def test_empty_password(self):
        response = self.client.post(self.login_url, {'username': 'testuser','password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter your password.', response.content.decode())
        # Empty password test

    def test_unknown_username(self):
        response = self.client.post(self.login_url, {'username': 'unknown','password': 'testpassword123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username or password.', response.content.decode())
        # Unknown user test