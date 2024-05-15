from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User
from django.contrib.messages import get_messages

class DeleteSectionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(username='admin', password='adminpass', role='Admin')
        self.course = Course.objects.create(course_id=100, course_name="Sample Course")
        self.section = Section.objects.create(course_parent=self.course, section_id=1)
        self.delete_url = reverse('deleteSection', kwargs={'pk': self.section.pk})
        self.login_url = reverse('login')

    def simulate_login(self, username, password):
        return self.client.post(self.login_url, {'username': username, 'password': password})

    def test_admin_can_access_delete_page(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_section.html')

    def test_confirm_deletion_by_admin(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.post(self.delete_url, {'confirm': 'yes'})
        self.assertRedirects(response, reverse('courseList'))
        self.assertFalse(Section.objects.filter(pk=self.section.pk).exists())

    def test_access_denied_for_non_admin(self):
        non_admin = User.objects.create(username='user', password='userpass', role='TA')
        self.simulate_login('user', 'userpass')
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('You are not authorized to view this page.', [msg.message for msg in messages])

    def test_attempt_to_delete_nonexistent_section(self):
        self.simulate_login('admin', 'adminpass')
        nonexistent_section_url = reverse('deleteSection', kwargs={'pk': 999})  # ID that does not exist
        response = self.client.post(nonexistent_section_url, {'confirm': 'yes'})
        self.assertEqual(response.status_code, 404)

    def test_delete_without_confirmation(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.post(self.delete_url)
        self.assertTrue(Section.objects.filter(pk=self.section.pk).exists())
        self.assertTemplateUsed(response, 'delete_section.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn('Section deleted successfully!', [msg.message for msg in messages])
