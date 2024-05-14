from django.test import TestCase, Client
from ta_app.models import User, Course


class EditCourse(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create(name='John Doe', username='jdoe', password='password123',
                                         email='jdoe@uwm.edu', role='Admin', phone_number='1234567890',
                                         address='Home', assigned=False)
        self.admin.save()

        # put a single course into the database.
        self.course = Course.objects.create(course_id=123,
                                            course_name='test course',
                                            description='this is a test',
                                            semester='Fall')

    def test_editCoursePageAdminAccess(self):
        # Test that the edit course page will load successfully with admin credentials
        resp = self.client.post("/login/", {"username": self.admin.username, "password": self.admin.password},
                                follow=True)
        self.assertRedirects(resp, "/Home/", 302, msg_prefix="unsuccessful login")
        resp = self.client.get(f"/Home/courseList/editCourse/{self.course.pk}/")
        self.assertEqual(200, resp.status_code, "role error")  # check that the courseCreate page loads

    def test_editCoursePageInstructorAccess(self):
        # Test that the edit course page will not load successfully if not an admin
        self.ins = User.objects.create(name='Jake Jones', username='jjones', password='password123',
                                       email='jjones@uwm.edu', role='Instructor', phone_number='1234567890',
                                       address='Home', assigned=False)
        self.ins.save()

        resp = self.client.post("/login/", {"username": self.ins.username, "password": self.ins.password},
                                follow=True)
        self.assertRedirects(resp, "/Home/", 302, msg_prefix="unsuccessful login")
        resp = self.client.get(f"/Home/courseList/editCourse/{self.course.pk}/")  # try to go to the editCourse page. Should not be allowed.
        self.assertRedirects(resp, "/Home/", 302,
                             msg_prefix="incorrectly allowed to access editCourse")

    def test_editCoursePageTAAccess(self):
        # Test that the edit course page will not load successfully if not an admin
        self.ta = User.objects.create(name='Jane Smith', username='jsmith', password='password123',
                                      email='jsmith@uwm.edu', role='Teacher-Assistant', phone_number='1234567890',
                                      address='Home', assigned=False)
        self.ta.save()

        resp = self.client.post("/login/", {"username": self.ta.username, "password": self.ta.password},
                                follow=True)
        self.assertRedirects(resp, "/Home/", 302, msg_prefix="unsuccessful login")
        resp = self.client.get(f"/Home/courseList/editCourse/{self.course.pk}/")
        self.assertRedirects(resp, "/Home/", 302,
                             msg_prefix="incorrectly allowed to access editCourse")

    def test_editCourseAllFieldsGood(self):
        data = {
            'course_id': 100,
            'course_name': 'new test name',
            'description': 'new test description',
            'semester': 'Spring'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.course.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!",
                         "Course was not edited correctly")
        self.assertEqual(1, Course.objects.all().count(), "An extra course was created when it should "
                                                          "not have been")
        # Now check that each altered field was properly updated in the database
        # Retrieve the most current version of the record from the database after editing using its known primary key
        course_from_db = Course.objects.get(pk=self.course.pk)
        self.assertEqual(100, course_from_db.course_id, "Course ID was not properly updated in the database")
        self.assertEqual('new test name', course_from_db.course_name, "Course name was not properly"
                                                                      " updated in the database")
        self.assertEqual('new test description', course_from_db.description, "Course description was not"
                                                                             " properly updated in the database")
        self.assertEqual('Spring', course_from_db.semester, "Course semester was not properly updated in"
                                                            " the database")

    def test_editCourseOnlyID(self):
        data = {
            'course_id': 100,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.course.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!", "Course was not "
                                                                                      "edited correctly")
        self.assertEqual(1, Course.objects.all().count(), "An extra course was created when it should "
                                                          "not have been")
        course_from_db = Course.objects.get(pk=self.course.pk)
        self.assertEqual(100, course_from_db.course_id, "Course ID was not properly updated in the database")

    def test_editCourseOnlyName(self):
        data = {
            'course_id': 123,
            'course_name': 'new test name',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.course.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!", "Course was not "
                                                                                      "edited correctly")
        self.assertEqual(1, Course.objects.all().count(), "An extra course was created when it should "
                                                          "not have been")
        course_from_db = Course.objects.get(pk=self.course.pk)
        self.assertEqual('new test name', course_from_db.course_name, "Course name was not properly "
                                                                      "updated in the database")

    def test_editCourseOnlyDescription(self):
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'new test description',
            'semester': 'Fall'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.course.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!", "Course was not "
                                                                                      "edited correctly")
        self.assertEqual(1, Course.objects.all().count(), "An extra course was created when it should not "
                                                          "have been")
        course_from_db = Course.objects.get(pk=self.course.pk)
        self.assertEqual('new test description', course_from_db.description, "Course description was not "
                                                                             "properly updated in the database")

    def test_editCourseOnlySemester(self):
        data = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Spring'
        }
        resp = self.client.post(f"/Home/courseList/editCourse/{self.course.pk}/", data)
        self.assertEqual(resp.context['errorMessage'], "Course edited successfully!","Course was not edited correctly")
        self.assertEqual(1, Course.objects.all().count(),"An extra course was created when it should not have been")
        course_from_db = Course.objects.get(pk=self.course.pk)
        self.assertEqual('Spring', course_from_db.semester, "Course semester was not properly updated in "
                                                            "the database")

    def test_editAllIntoConflict(self):
        data = {
            'course_id': 100,
            'course_name': 'new test name',
            'description': 'new test description',
            'semester': 'Spring'
        }
        resp = self.client.post('/Home/createCourse/', data)  # create a second entry
        edit = {
            'course_id': 123,
            'course_name': 'test course',
            'description': 'this is a test',
            'semester': 'Fall'
        }
        # unfinished
