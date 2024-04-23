from django.test import TestCase
from ta_app.models import Section, Course
from django.utils import timezone
from ta_app.Classes.SectionClass import SectionClass



class Test_SectionClass(TestCase):
    def setUp(self):
        # Set up initial test data
        self.course = Course.objects.create(course_id=30311, course_name='compsci', description='cs')  # course_id should be an integer
        self.meeting_time = timezone.now().replace(hour=15, minute=0, second=0, microsecond=0)

        # Create sections
        self.section1 = Section.objects.create(
            course_parent=self.course,
            section_id=12307,  # Ensure this matches the expected integer type in your model
            meeting_time=self.meeting_time,
            type='lec',
        )
        self.section2 = Section.objects.create(course_parent=self.course, section_id=234,
                                               meeting_time=self.meeting_time, type='LAB')
        self.section3 = Section.objects.create(course_parent=self.course, section_id=334,
                                               meeting_time=self.meeting_time, type='DIS')  # Assuming 'DIS' as a type
        self.section4 = Section.objects.create(course_parent=self.course, section_id=445,
                                               meeting_time=self.meeting_time, type='SEM')  # Assuming 'SEM' as a type


    def test_section_creation(self):
        self.assertIsNotNone(self.section1)
        self.assertIsNotNone(self.section2)
        self.assertIsNotNone(self.section3)
        self.assertIsNotNone(self.section4)

    def test_duplicate_section_creation(self):
        duplicate_section = SectionClass(
            course_parent=self.section1.course_parent,
            section_id=self.section1.section_id,
            meeting_time=self.section1.meeting_time,
            section_type=self.section1.type
        )

        with self.assertRaises(ValueError):
            duplicate_section.create_section()

    def test_None_section_creation(self):
        with self.assertRaises(ValueError):
            SectionClass(course_parent=None, section_id=None, meeting_time=None, section_type=None)




    def test_edit_section_id(self):
        new_id = 10
        self.section1.section_id = new_id
        self.section1.save()
        self.assertEqual(self.section1.section_id, new_id)

    def test_edit_meeting_time(self):
        new_time = timezone.now().replace(hour=10, minute=0)
        self.section2.meeting_time = new_time
        self.section2.save()
        self.assertEqual(self.section2.meeting_time, new_time)

    def test_edit_type(self):
        new_type = 'TUT'  # Assuming 'TUT' as another type
        self.section3.type = new_type
        self.section3.save()
        self.assertEqual(self.section3.type, new_type)

    def test_delete_section(self):
        section_id = self.section4.section_id
        self.section4.delete()
        with self.assertRaises(Section.DoesNotExist):
            Section.objects.get(section_id=section_id)
