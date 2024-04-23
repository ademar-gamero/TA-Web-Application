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
        response = self.client.post("/accountCreation/", {'username': 'admin', 'password': 'pass', 'name': 'Test Admin',
                                                          'role': 'Instructor', 'email': 'email@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Username is already taken", "did not catch duplicate username")

    def test_createAccountBadEmail(self):
        response = self.client.post("/accountCreation/", {'username': 'new2', 'password': 'pass', 'name': 'Name2',
                                                          'role': 'Instructor', 'email': 'words',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Invalid email address", "did not catch bad email")

    def test_createEmpty(self):
        response = self.client.post("/accountCreation/", {'username': '', 'password': '', 'name': '',
                                                          'role': '', 'email': '',
                                                          'phone_number': '', 'address': ''})
        self.assertEqual(response.context['message'],
                         "Must include username, password, name, role, and email.",
                         "did not catch empty fields")

    def test_createAccountSpaceInUsername(self):
        response = self.client.post("/accountCreation/", {'username': 'new 2', 'password': 'pass', 'name': 'Name2',
                                                          'role': 'Instructor', 'email': 'test@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Username cannot contain spaces", "did not catch bad username")

    def test_createAccountSpaceInPassword(self):
        response = self.client.post("/accountCreation/", {'username': 'new2', 'password': 'pass new', 'name': 'Name2',
                                                          'role': 'Instructor', 'email': 'test@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Password cannot contain spaces", "did not catch bad password")
