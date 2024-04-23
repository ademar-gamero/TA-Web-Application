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
        response = self.client.post("/accountCreation/", {'username': 'new', 'password': 'pass', 'name': 'Name',
                                                          'role': 'Instructor', 'email': 'email@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertTrue(User.objects.exists(username='new'), "User was not created")

    def test_createAccountDuplicate(self):
        response = self.client.post("/accountCreation/", {'username': 'admin', 'password': 'pass', 'name': 'Name',
                                                          'role': 'Instructor', 'email': 'email@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Username is already taken", "did not catch duplicate username")

    def test_createAccountBadEmail(self):
        response = self.client.post("/accountCreation/", {'username': 'admin', 'password': 'pass', 'name': 'Name',
                                                          'role': 'Instructor', 'email': 'words',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Invalid email address", "did not catch bad email")

