from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import User
from django.contrib.messages import get_messages

class DeleteAccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(username='admin', password='adminpass', name='admin', email='admin@aol.com', role='Admin', assigned=False)
        self.user = User.objects.create(username='user1', password='userpass', name='test', email='tezt@uwm.edu', role='Teacher-Assistant', assigned=False, skills='')
        self.delete_url = reverse('deleteAccount', kwargs={'pk': self.user.id})
        self.login_url = reverse('login')

    def simulate_login(self, username, password):
        return self.client.post(self.login_url, {'username': username, 'password': password})

    def test_admin_can_access_delete_page(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_account.html')

    def test_confirm_deletion_by_admin(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.post(self.delete_url, {'confirm': 'yes'})
        self.assertRedirects(response, reverse('accountList'))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_access_denied_for_non_admin(self):
        self.simulate_login('user1', 'userpass')
        response = self.client.get(self.delete_url)
        self.assertNotEqual(response.status_code, 200)  # Expected redirection or access denied
        self.assertTrue(any(msg.message == 'You are not authorized to view this page.' for msg in get_messages(response.wsgi_request)))

    def test_attempt_to_delete_nonexistent_account(self):
        self.simulate_login('admin', 'adminpass')
        nonexistent_user_url = reverse('deleteAccount', kwargs={'pk': 999})  # ID that does not exist
        response = self.client.post(nonexistent_user_url, {'confirm': 'yes'})
        self.assertEqual(response.status_code, 404, "Expected a 404 status for a nonexistent account.")

    def test_delete_without_confirmation(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.post(self.delete_url)  # Posting without the 'confirm' key
        self.assertTrue(User.objects.filter(id=self.user.id).exists(),
                        "User should still exist if deletion is not confirmed.")
        self.assertTemplateUsed(response, 'delete_account.html',
                                "Confirm page should still be shown when deletion is not confirmed.")
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue('Account deleted successfully!' not in [msg.message for msg in messages],
                        "No deletion success message should be present.")


