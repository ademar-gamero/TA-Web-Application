from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, User, Section
from django.contrib.messages import get_messages

class DeleteSectionTests(TestCase):
    def setup(self):
        self.client = Client()
        self.admin = User.objects.create(username='admin', password='adminpass', role='Admin')
        self.course = Course.objects.create(course_id=100, course_name="Sample Course")
        self.section = Section.objects.create(section_name="Sample Section", section_id=200, course_id=self.course)
        self.course.save()
        self.delete_url = reverse('deleteSection', kwargs={'section_id': self.section.pk})
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
        response = self.client.post(self.delete_url, {'confirm': '1'})
        self.assertRedirects(response, reverse('courseList'))
        self.assertEqual(Course.objects.count(), 0)

    def test_access_denied_for_non_admin(self):
        non_admin = User.objects.create(username='user', password='userpass', role='TA')
        self.simulate_login('user', 'userpass')
        response = self.client.get(self.delete_url)
        self.assertRedirects(response, reverse('courseList'), status_code=302, target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('You are not authorized to view this page.', [msg.message for msg in messages])

    def test_attempt_to_delete_nonexistent_account(self):
        self.simulate_login('admin', 'adminpass')
        nonexistent_user_url = reverse('deleteAccount', kwargs={'pk': 999})  # ID that does not exist
        response = self.client.post(nonexistent_user_url, {'confirm': 'yes'})
        self.assertRedirects(response, reverse('accountList'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'User account not found!')

    def test_delete_without_confirmation(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.post(self.delete_url)
        self.assertEqual(Course.objects.count(), 1)
        self.assertRedirects(response, reverse('courseList'))