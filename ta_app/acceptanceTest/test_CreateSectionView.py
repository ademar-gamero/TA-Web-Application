from datetime import time, datetime

from django.test import TestCase
from django.test import Client
from ta_app.models import Section, Course, User,Day
from ta_app.Classes.SectionClass import SectionClass

class AcceptanceTestSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(course_name='Intro to CompSci',
                                            course_id=30311, description='Introductory',
                                            semester='Fall')
        self.course.save()
        self.section1 = Section.objects.create(course_parent=self.course, section_id=123,
                                              start_time=time(9, 30),end_time=time(10, 20),type='LEC',location= 'ems180',is_online=False)
        self.monday = Day.objects.create(day="MO")
        self.tuesday = Day.objects.create(day="TU")
        self.wednesday = Day.objects.create(day="WE")
        self.thursday = Day.objects.create(day="TH")
        self.friday = Day.objects.create(day="FR")
        self.monday.save()
        self.tuesday.save()
        self.wednesday.save()
        self.thursday.save()
        self.friday.save()
        self.section1.meeting_days.add(self.monday, self.wednesday)
        self.section1.save()
        self.green= Client()
        self.admin = User(name="admin", username="admin", password="admin", email="admin@email.com", role="Admin",
                          phone_number=1, address="1", assigned=False).save()
        self.instructor= User(name="ins", username="ins", password="ins", email="admin@email.com", role="Instructor",
                            phone_number=1, address="1", assigned=False).save()
        self.ta = User(name="ta", username="ta", password="ta", email="admin@email.com", role="TA",
                            phone_number=1, address="1", assigned=False).save()


    def test_courseNotFound(self):
        day_pk = []
        for day in self.section1.meeting_days.all():
            day_pk.append(day.pk)
        self.client.login(username='admin', password='admin')
        resp= self.client.get("/Home/createSection/")
        self.assertEqual(200, resp.status_code, "status code is not 200")
        post_data= {'course_parent': 12345, 'section_id': self.section1.section_id,
                    'start_time': "9:30", 'end_time': "10:20",
                    'section_type': self.section1.type, 'location': self.section1.location,
                    'is_online': self.section1.is_online, 'days': day_pk}
        resp= self.client.post('/Home/createSection/', post_data)
        self.assertEqual(200, resp.status_code, "status code is not 200")
        self.assertEqual("Course not found", resp.context['error'], "error message is not correct")

    def test_section_added(self):
        Section.objects.all().delete()
        response = self.client.post('/Home/createSection/', {
            'course_parent': self.course.pk,  # Use the course ID
            'section_id': 123,
            'start_time': "9:30",
            'end_time': "10:20",
            'section_type': 'LEC',
            'location': 'ems180',
            'is_online': False,
            'days': [self.monday.pk, self.wednesday.pk]
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], "Section created successfully",
                         "Section was not created when it should have been.")



    def test_section(self):
        resp=self.green.post("/login/", {"username": 'admin', "password": 'admin'}, follow=True)
        resp= self.green.get("/Home/createSection/")
        self.assertEqual(200, resp.status_code)
        resp=self.green.get(self.section1.section_id)
        self.assertEqual(404, resp.status_code)
        resp = self.green.post(self.section1.section_id, {'course_parent': self.course.pk, 'section_id': 123,
                                                 'start_time': "9:30",
                                                 'end_time': "10:20",
                                                 'section_type': 'LEC', 'location': 'ems180',
                                                 'is_online': False, 'days': [self.monday.id, self.wednesday.id]})
        self.assertEqual(404, resp.status_code)
        message = resp.context.get('message')
        if message is not None:
            self.assertEqual(message, "Section created successfully")


    def test_sectionDisplay(self):
        response = self.client.post('/Home/createSection/', {
            'course_parent': self.course.pk,  # Use the course ID
            'section_id': 123,
            'start_time': "9:30",
            'end_time': "10:20",
            'section_type': 'LAB',
            'location': 'ems180',
            'is_online': False,
            'days': [self.monday.pk, self.wednesday.pk]
        })

        sec = Section.objects.get(section_id=123)
        res = response.context["sections"]
        self.assertTrue(sec in res, "value was not displayed")

    # make a test for test saved sections table (multiple things in context)
    def test_sameEverythingExceptId(self):
        response = self.client.post('/Home/createSection/', {
            'course_parent': self.course.pk,
            'section_id': 27747,
            'start_time': "9:30",
            'end_time': "10:20",
            'section_type': 'LAB',
            'location': 'ems180',
            'is_online': False,
            'days': [self.monday.pk, self.wednesday.pk]
        })
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual("Section created successfully", response.context['error'], "Section was not created when it should have been.")

        response = self.client.post('/Home/createSection/', {
            'course_parent': self.course.pk,
            'section_id': 2525,
            'start_time': "9:30",
            'end_time': "10:20",
            'section_type': 'LAB',
            'location': 'ems180',
            'is_online': False,
            'days': [self.monday.pk, self.wednesday.pk]
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual("Section in the same location and at same time can not be added.", response.context['error'])

    def tes_improperCourseID(self):
        response = self.client.post('/Home/createSection/', {
            'course_parent': self.course,
            'section_id': 2525,
            'start_time': "9:30",
            'end_time': "10:30",
            'section_type': 'LAB',
            'location': 'ems180',
            'is_online': False,
            'days': [self.monday.pk, self.wednesday.pk]
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual("Field 'course_id' expected a number but got '30311 Intro to CompSci - Fall'.", response.context['error'],)


    def test_invalidSectionDisplay(self):
        size_before = Section.objects.all().count()
        response = self.client.post('/Home/createSection/', {
            'course_parent': 'ee',
            'section_id': 123,
            'start_time': "9:30",
            'end_time': "10:20",
            'section_type': 'LEC',
            'location': 'ems180',
            'is_online': False,
            'days': [self.monday.pk, self.wednesday.pk]  # Use the IDs of the Day objects
        }, follow=True)

        clist = response.context['sections']
        size = len(clist)
        self.assertTrue(size == size_before, "invalid section was displayed")
