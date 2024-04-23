from django.test import TestCase
from django.urls import reverse
from ta_app.models import User

class AccountCreationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='admin',
            password='password',
            email='test@example.com',
            name='Test Admin',
            role='Administrator'
        )
    def test_createAccount(self):
        response = self.client.post(reverse(''))
