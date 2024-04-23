from django.test import TestCase
from django.test import Client
from ta_app.models import Section, Course

class AcceptanceTestSection(TestCase):
    def setUp(self):
        self.client = Client()
        self.course = Course.objects.create(course_name='Intro to CompSci', course_id=30311, description='Introductory')
        self.section = Section.objects.create(course_parent=self.course, section_id=123, meeting_time='2023-01-01T14:00:00Z', type='LEC')

    def test_no_section(self):
        # Deleting the section to simulate no sections existing
        Section.objects.all().delete()
        response = self.client.post('/Home/createSection/',{'course_id':self.course.id})
        # Check if the page returns the expected status when no sections are available
        self.assertEqual(response.status_code, 200)
        response= self.client.get('/Home/createSection/',{'course_id':self.course.id})
        # Check for specific error message in the response context
        self.assertEqual(response.context['error'], 'No section exist yet...')

    def test_section_creation(self):
        # Simulate creating a section via POST request
        data = {
            'course_parent': self.course.id,
            'section_id': 2,
            'meeting_time': '2023-01-01T15:00:00Z',
            'type': 'LAB'
        }
        response = self.client.post('/Home/createSection/', data, follow=True)
        # Verify redirection after successful creation
        self.assertRedirects(response, '/Home/createSection/')
        # Verify the section creation
        self.assertTrue(Section.objects.filter(section_id=2).exists())

        # Fetching the newly created section to verify its presence
        response = self.client.get('/Home/createSection/')
        # Assuming context provides a list of sections
        all_sections = [str(section) for section in response.context['sections']]
        expected_section_str = f'{self.course.course_name} LAB 2'
        self.assertIn(expected_section_str, all_sections)
    def test_duplicate_section(self):
        # Trying to create a duplicate section with the same section_id and course
        response = self.client.post('/Home/createSection/', {
            'course_parent': self.course.id,
            'section_id': 123,
            'meeting_time': '2023-01-01T15:00:00Z',
            'type': 'LEC'
        }, follow=True)
        # Check that the page does not redirect and checks for a duplication error
        self.assertEqual(response.status_code, 200)
        # Assuming the context provides an error message for duplicate section
        self.assertEqual(response.context['error'], 'Section with this ID already exists.')