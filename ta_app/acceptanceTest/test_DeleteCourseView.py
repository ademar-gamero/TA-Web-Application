from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, User

class DeleteCourseAcceptanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(username='admin', password='adminpass', role='Admin')
        self.admin.save()
        self.course = Course.objects.create(course_id=361, course_name="CS")
        self.course.save()

    def test_admin_can_access_delete_page(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('deleteCourse', args=[self.course.pk]))
        self.assertEqual(response.status_code, 200)

    def test_confirm_deletion(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('deleteCourse', args=[self.course.pk]), {'confirm': '1'})
        self.assertRedirects(response, reverse('courseList'))
        self.assertEqual(Course.objects.count(), 0)