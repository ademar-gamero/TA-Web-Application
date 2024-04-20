from django.test import TestCase
from ta_app.models import User, Roles
from django.urls import reverse

class LoginTests(TestCase):
    def setUp(self):
        user = User.objects.create(
            name="Test User",
            username="testuser",
            email="test@example.com",
            role=Roles.AD,
            phone_number="1234567890",
            address="123 Test St"
        )
        user.set_password("password123")
        user.save()
        self.login_url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_login_unknown_user(self):
        response = self.client.post(self.login_url, {
            'username': 'unknownuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_login_empty_username(self):
        response = self.client.post(self.login_url, {
            'username': '',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')

    def test_login_empty_password(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password', 'This field is required.')