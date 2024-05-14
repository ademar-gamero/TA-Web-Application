
from datetime import time
from django.test import TestCase, Client
from django.urls import reverse

from ta_app.Classes.SectionClass import SectionClass
from ta_app.models import Section, Course, User, Day

#navigation part:
    #1.go to the editsectionview page
    #role validation part:
    #2.check role of the user
    #3.check if the user is an admin
    # editting part:
    #4.get the section object
    #5.calling post on editsectionview
    #6.get the section object again
    #7.check if the section is edited properly
    #8.check if the message is displayed properly
class EditSectionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(course_name='Intro to CompSci',
                                            course_id=30311, description='Introductory',
                                            semester='Fall')
        self.course.save()

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
        self.admin = User.objects.create(name="admin", username="admin", password="admin", email="admin@email.com", role="Admin",
                          phone_number=1, address="1", assigned=False)
        self.admin.save()
        self.instructor = User.objects.create(name="ins", username="ins", password="ins", email="admin@email.com", role="Instructor",
                               phone_number=1, address="1", assigned=False)
        self.instructor.save()
        self.ta = User.objects.create(name="ta", username="ta", password="ta", email="admin@email.com", role="TA",
                       phone_number=1, address="1", assigned=False)
        self.ta.save()
        self.section1 = SectionClass(course_parent=self.course, section_id=100,
                                     start_time='09:30', end_time='10:20', section_type='LEC',
                                     location='ems180', is_online=False, meeting_days=[self.monday, self.wednesday])
        self.section1.create_section()
        self.section2 = SectionClass(course_parent=self.course, section_id=200,
                                     start_time='10:30', end_time='11:20', section_type='LEC',
                                     location='ems190', is_online=False, meeting_days=[self.monday, self.wednesday])
        self.section2.create_section()
        self.section3 = SectionClass(course_parent=self.course, section_id=300,
                                     start_time='11:30', end_time='12:20', section_type='LEC',
                                     location='ems200', is_online=False, meeting_days=[self.monday, self.wednesday])
        self.section3.create_section()
        self.obj = Section.objects.get(section_id=self.section1.section_id)
        self.detail_url_course = reverse('editSection', args=[self.obj.pk])

    def test_navigation_to_edit_page(self):
        resp = self.client.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        response = self.client.get(reverse('editSection', kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {'username': self.admin.username, 'password': self.admin.password},
                                    follow=True)
        self.assertRedirects(response, reverse('Home'))
        self.assertTrue('role' in self.client.session and self.client.session['role'] == 'Admin')
        self.assertTrue('name' in self.client.session and self.client.session['name'] == self.admin.name)
        resp = self.client.get(self.detail_url_course, follow=True)
        self.assertEqual(resp.status_code, 200)
    def test_ta_validation(self):
        resp = self.client.post('/login/',{"username":self.ta.username,"password":self.ta.password},follow=True)
        resp = self.client.get(self.detail_url_course, follow=True)
        self.assertRedirects(resp, "/Home/", msg_prefix="unsuccessful role validation")
    def test_instructor_validation(self):
        resp = self.client.post('/login/',{"username":self.instructor.username,"password":self.instructor.password},follow=True)
        resp = self.client.get(self.detail_url_course, follow=True)
        self.assertRedirects(resp, "/Home/", msg_prefix="unsuccessful role validation")
    def test_edit_section(self):
        resp = self.client.post(
            "/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        post_data = {
            'course_parent': self.course.pk,
            'section_id': self.section1.section_id,
            'start_time': '10:00',
            'end_time': '11:00',
            'section_type': 'lab',
            'location': 'EMS102',
            'is_online': '',
            'meeting_days': [self.monday.day, self.wednesday.day]
        }
        resp = self.client.post(self.detail_url_course, post_data, follow=True)
        self.assertEqual(resp.status_code, 200)

        updated_section = Section.objects.get(pk=self.obj.pk)
        self.assertEqual(updated_section.type, 'lab')
        self.assertEqual(updated_section.location, 'EMS102')
        self.assertFalse(updated_section.is_online)
        self.assertEqual(updated_section.start_time, time(10, 0))
        self.assertEqual(updated_section.end_time, time(11, 0))
        self.assertIn(self.monday, updated_section.meeting_days.all())
        self.assertIn(self.wednesday, updated_section.meeting_days.all())
        self.assertIn(self.wednesday, updated_section.meeting_days.all())
    def test_invalid_is_online(self):
        resp = self.client.post(
            "/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        post_data = {
            'course_parent': self.course.pk,
            'section_id': self.section1.section_id,
            'start_time': '10:00',
            'end_time': '11:00',
            'section_type': 'Lab',
            'location': 'EMS102',
            'is_online': '1',
            'meeting_days': [self.monday.day, self.wednesday.day]
        }
        resp = self.client.post(self.detail_url_course, post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual("Please enter 'None' in location for online classes", resp.context['message'])
    def test_noLocation_given(self):
        resp = self.client.post(
            "/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        post_data = {
            'course_parent': self.course.pk,
            'section_id': self.section1.section_id,
            'start_time': '10:00',
            'end_time': '11:00',
            'section_type': 'Lab',
            'location':'None' ,
            'is_online': '',
            'meeting_days': [self.monday.day, self.wednesday.day]
        }
        resp = self.client.post(self.detail_url_course, post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual("Location must be provided for in-person classes", resp.context['message'])
    def test_noMeetingdays_given(self):
        resp = self.client.post(
            "/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        post_data = {
            'course_parent': self.course.pk,
            'section_id': self.section1.section_id,
            'start_time': '10:00',
            'end_time': '11:00',
            'section_type': 'Lab',
            'location':'ems201' ,
            'is_online': '',
        }
        resp = self.client.post(self.detail_url_course, post_data, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual("Meeting days must be provided for in-person classes", resp.context['message'])
