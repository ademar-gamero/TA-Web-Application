from django.test import TestCase
from classes.InstructorClass import Instructor
from ta_app.models import Section, User, Roles


class TestInstructorClass(TestCase):
    def setUp(self):
        # Create an Instructor and a Section for testing
        self.instructor = Instructor(
            username='johndoe',
            password='password123',
            name='John Doe',
            email='johndoe@example.com',
            phone_number='555-555-5555',
            address='1234 Elm Street'
        )
        self.section = Section(
            course_parent_id=1,  # assuming a course with ID 1 exists
            section_id=101,
            meeting_time='2023-01-01 09:00',
            type='LEC'
        )
        # Simulate saving the section (in a real test, this would hit the DB)
        self.section.id = 1

        self.ta = User(
            name='Jane Doe',
            username='janedoe',
            password='password123',
            email='janedoe@example.com',
            role=Roles.TA,
            phone_number='555-555-5555',
            address='1234 Maple Street'
        )
        # Simulate saving the TA (in a real test, this would hit the DB)
        self.ta.id = 1

    def test_set_contact_info(self):
        # Test setting contact info
        new_email = 'johnupdate@example.com'
        new_phone = '111-111-1111'
        new_address = '4321 Oak Street'
        self.instructor.set_contact_info(new_email, new_phone, new_address)

        self.assertEqual(self.instructor.email, new_email)
        self.assertEqual(self.instructor.phone_number, new_phone)
        self.assertEqual(self.instructor.address, new_address)

    def test_assign_ta_to_section(self):
        # Test assigning a TA to a section
        self.instructor.assign_TA_to_section(self.ta, self.section)
        # Assuming you have a method to check assigned TAs
        self.assertIn(self.ta, self.section.tas.all())  # This would normally require a DB call

    def test_str_representation(self):
        # Test the string representation of the instructor
        expected_representation = f'{self.instructor.name} : {self.instructor.role}'
        self.assertEqual(str(self.instructor), expected_representation)

