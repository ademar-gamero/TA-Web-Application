from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User
from django.contrib.messages import get_messages

class RemoveCourseTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(username='admin', password='adminpass', role='Admin')
        self.course = Course.objects.create(course_id=100, course_name="Sample Course")
        self.section = Section.objects.create(course_parent=self.course, section_id=1)
        self.user = User.objects.create(username='user', password='userpass', role='Teacher-Assistant', name="Frank", email="email@e.com")
        self.user.assigned_section.add(self.section)
        self.remove_url = reverse('removeCourseAssignment', kwargs={'user_pk': self.user.pk, 'course_pk': self.course.pk})
        self.login_url = reverse('login')

    def simulate_login(self, username, password):
        return self.client.post(self.login_url, {'username': username, 'password': password})

    def test_admin_can_access_remove_page(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.get(self.remove_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'remove_courseAssignment.html')

    def test_confirm_removal_by_admin(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.post(self.remove_url, {'confirm': 'yes'})
        #self.assertRedirects(response, reverse('courseList'))
        self.assertFalse(self.section in self.user.assigned_section.all())

    def test_access_denied_for_non_admin(self):
        non_admin = User.objects.create(username='user1', password='user1pass', role='TA')
        self.simulate_login('user1', 'user1pass')
        response = self.client.get(self.remove_url)
        self.assertRedirects(response, reverse('courseList'), status_code=302, target_status_code=200)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn('You are not authorized to view this page.', [msg.message for msg in messages])

    def test_attempt_to_remove_nonexistent_course(self):
        self.simulate_login('admin', 'adminpass')
        nonexistent_section_url = reverse('removeCourseAssignment', kwargs={'user_pk': self.user.pk, 'course_pk': 999})  # ID that does not exist
        response = self.client.post(nonexistent_section_url, {'confirm': 'yes'})
        self.assertEqual(response.status_code, 404)

    def test_remove_without_confirmation(self):
        self.simulate_login('admin', 'adminpass')
        response = self.client.post(self.remove_url)
        self.assertTrue(self.section in self.user.assigned_section.all())
        self.assertTemplateUsed(response, 'remove_section.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertNotIn('Removed from section!', [msg.message for msg in messages])
