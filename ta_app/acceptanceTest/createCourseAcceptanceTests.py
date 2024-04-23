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
        # Test creating a single course successfully
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'This is a test course.'
        }
        self.client.post("/login/", {"username": self.admin.username, "password": self.admin.password},
                         follow=True)  # try login
        resp = self.client.post('/Home/createCourse/', data)
        self.assertTrue(resp.context['check'], "Course did not create correctly")


class CreateMultipleCourses(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(name='John Doe', username='jdoe', password='password123',
                                         email='jdoe@uwm.edu', role='Admin', phone_number='1234567890',
                                         address='Home', assigned=False)
        self.admin.save()
        # put a single course into the database
        Course.objects.create(course_id=123, course_name='test course', description='This is a test').save()

    def test_createMultipleDifferent(self):
        # will adding multiple courses with all different fields create separate entries in the database?
        data = {
            'course_id': 361,
            'course_name': 'CompSci',
            'description': 'This is a computer science course.'
        }
        resp = self.client.post('/Home/createCourse/', data)  # try adding again
        self.assertTrue(resp.context['check'], "Course did not create correctly")
        # check the count of all courses in the database. (It should increase. Refer to test_createCourseSuccess
        # for the results single create course.)
        self.assertEqual(2, Course.objects.all().count(), "New course was not created")

    def test_createDuplicateCourse(self):
        # will trying to add a course with all duplicate fields (ie. same course) update the database?
        # Note: same data as the course created in setUp
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'This is a test course.'
        }
        resp = self.client.post('/Home/createCourse/', data)  # try adding again
        self.assertFalse(resp.context['check'], "Duplicate course was incorrectly added")
        # check the count of all courses in the database
        self.assertEqual(1, Course.objects.all().count(), "Duplicate course was added")  # should not increase

    def test_createTwoWithOnlySameName(self):
        # will trying to add another course with the same course_name but different course_id and description be allowed?
        data = {
            'course_id': 100,
            'course_name': 'test course',
            'description': 'A different test course.'
        }
        resp = self.client.post('/Home/createCourse/', data)
        self.assertTrue(resp.context['check'], "Course did not create correctly")
        self.assertEqual(2, Course.objects.all().count(), "New course was not created")

    def test_createTwoWithOnlySameId(self):
        # will trying to add another course with the same course_id but different course_name and description be allowed?
        data = {
            'course_id': 123,
            'course_name': 'new name',
            'description': 'A different test course.'
        }
        resp = self.client.post('/Home/createCourse/', data)
        self.assertTrue(resp.context['check'], "Course did not create correctly")
        self.assertEqual(2, Course.objects.all().count(), "New course was not created")  # should increase

    def test_createTwoWithOnlyDifferentDescription(self):
        # will trying to add another course with the same course_id but different course_name and description be allowed?
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'A different test course.'
        }
        resp = self.client.post('/Home/createCourse/', data)
        self.assertFalse(resp.context['check'], "Course did not create correctly")
        self.assertEqual(1, Course.objects.all().count(), "New course was not created")  # should not increase


