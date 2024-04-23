from django.test import TestCase
from django.test import Client
from ta_app.models import Section, Course, User
from ta_app.classes.SectionClass import SectionClass

class AcceptanceTestSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(course_name='Intro to CompSci', course_id=30311, description='Introductory')
        self.course.save()
        self.section = Section.objects.create(course_parent=self.course, section_id=123, meeting_time='2023-01-01T14:00:00Z', type='LEC')
        self.green = Client()
        self.admin = User(name="admin", username="admin", password="admin", email="admin@email.com", role="Admin",
                          phone_number=1, address="1", assigned=False).save()
        self.instructor = User(name="ins", username="ins", password="ins", email="admin@email.com", role="Instructor",
                          phone_number=1, address="1", assigned=False).save()
    def test_duplicate_section(self):
        Section.objects.all().delete()
       # resp = self.green.post("/login/", {"username": 'admin',"password": 'admin'}, follow=True)
        #self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/createSection/")
        resp = self.client.post('/Home/createSection/',{'course_parent':self.course,'section_id':self.section.section_id,'meeting_time':self.section.meeting_time,'section_type':self.section.type})
        # Check if the page returns the expected status when no sections are available
        self.assertEqual(resp.status_code, 200)

        check_value = resp.context['check']
        self.assertFalse(check_value,'Section already exists')

    def test_section_added(self):
        Section.objects.all().delete()
        response = self.client.post('/Home/createSection/', {
            'course_parent': self.course.id,  # Use the course ID
            'section_id': 27747,
            'meeting_time': '2023-01-01T14:00:00Z',
            'section_type': 'LAB'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['check'], "Section was not created when it should have been.")

    def test_section(self):
        response = self.client.post('/Home/createSection/', {
            'course_parent': 'ee',
            'section_id': 123,
            'meeting_time': '2023-01-01T15:00:00Z',
            'section_type': 'LEC'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['check'], "Section was not created when it should have been.")