from django.test import TestCase, Client

from ta_app.models import User, Course


class CreateCourseAcceptanceTests(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(name='John Doe', username='jdoe', password='password123',
                                         email='jdoe@uwm.edu', role='Admin', phone_number='1234567890',
                                         address='Home', assigned=False)
        self.admin.save()

    def test_createCoursePageLoads(self):
        # Test that the create course page will load successfully
        resp = self.client.post("/login/", {"username": self.admin.username, "password": self.admin.password},
                                follow=True)
        self.assertRedirects(resp, "/Home/", 302, msg_prefix="unsuccessful login")
        resp = self.client.get("/Home/createCourse/")
        self.assertEqual(200, resp.status_code, "role error")  # check that the courseCreate page loads

    def test_createCourseSuccess(self):
        # Test creating a course successfully
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'This is a test course.'
        }
        self.client.post("/login/", {"username": self.admin.username, "password": self.admin.password},
                         follow=True)  # try login
        resp = self.client.post('/Home/createCourse/', data)
        self.assertTrue(resp.context['check'], "Course did not create correctly")

    def test_createDuplicateCourse(self):
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'This is a test course.'
        }
        self.client.post("login/", {"username": self.admin.username, "password": self.admin.password},
                         follow=True)  # try login
        self.client.post('/Home/createCourse/', data)
        resp = self.client.post('/Home/createCourse/', data)  # try adding again
        self.assertEqual(1, Course.objects.all().count(), "Duplicate course was added")
