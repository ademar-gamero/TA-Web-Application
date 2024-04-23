from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import User


class AccountCreationTests(TestCase):

    client = None
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(
            username='admin',
            password='password',
            email='test@example.com',
            name='Test Admin',
            role='Admin'
        )
        self.user = User.objects.create(
            username='other',
            password='password',
            email='2@test.com',
            name='Test User',
            role='Instructor'
        )

    def test_roleValidationCorrect(self):
        response = self.client.post("/login/", {'username': 'admin', 'password': 'password'}, follow=True)
        self.assertRedirects(response, reverse('Home'))
        response = self.client.get("/Home/accountCreation/")
        self.assertEqual(200, response.status_code, "role validation failed")

    def test_roleValidationIncorrect(self):
        response = self.client.post("/login/", {'username': 'other', 'password': 'password'}, follow=True)
        self.assertRedirects(response, reverse('Home'))
        response = self.client.get("/Home/accountCreation/")
        self.assertEqual(302, response.status_code, "role validation failed")

    def test_createAccount(self):
        response = self.client.post("/Home/accountCreation/", {'username': 'new', 'password': 'pass', 'name': 'Name',
                                                          'role': 'Instructor', 'email': 'email@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertTrue(User.objects.filter(username="new").exists(), "User was not created")

    def test_createAccountSparse(self):
        response = self.client.post("/Home/accountCreation/", {'username': 'new', 'password': 'pass', 'name': 'Name',
                                                          'role': 'Instructor', 'email': 'email@email.com',
                                                          'phone_number': '', 'address': ''})
        self.assertTrue(User.objects.filter(username="new").exists(), "User was not created")

    def test_createAccountDuplicate(self):
        response = self.client.post("/Home/accountCreation/", {'username': 'admin', 'password': 'pass', 'name': 'Test Admin',
                                                          'role': 'Instructor', 'email': 'email@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Username is already taken", "did not catch duplicate username")

    def test_createAccountBadEmail(self):
        response = self.client.post("/Home/accountCreation/", {'username': 'new2', 'password': 'pass', 'name': 'Name2',
                                                          'role': 'Instructor', 'email': 'words',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Email is not valid", "did not catch bad email")

    def test_createAccountBadRole(self):
        response = self.client.post("/Home/accountCreation/", {'username': 'Zog', 'password': 'pass', 'name': 'Zog',
                                                          'role': 'Barbarian', 'email': 'words',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Invalid role", "did not catch bad role")

    def test_createEmpty(self):
        response = self.client.post("/Home/accountCreation/", {'username': '', 'password': '', 'name': '',
                                                          'role': '', 'email': '',
                                                          'phone_number': '', 'address': ''})
        self.assertEqual(response.context['message'],
                         "Must include username, password, name, role, and email.",
                         "did not catch empty fields")

    def test_createAccountSpaceInUsername(self):
        response = self.client.post("/Home/accountCreation/", {'username': "new 2", 'password': 'pass', 'name': 'Name2',
                                                          'role': 'Instructor', 'email': 'test@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Username cannot contain spaces", "did not catch bad username")

    def test_createAccountSpaceInPassword(self):
        response = self.client.post("/Home/accountCreation/", {'username': 'new2', 'password': 'pass new', 'name': 'Name2',
                                                          'role': 'Instructor', 'email': 'test@email.com',
                                                          'phone_number': '1234567890', 'address': '123 Fake Street'})
        self.assertEqual(response.context['message'], "Password cannot contain spaces", "did not catch bad password")
