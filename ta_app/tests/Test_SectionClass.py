from django.core.exceptions import ValidationError
from ta_app.Classes.SectionClass import SectionClass
from ta_app.models import Section, Course, Day
from datetime import time,datetime
from django.test import TestCase

class Test_SectionClass(TestCase):
    def setUp(self):
        # Create courses
        self.course1 = Course.objects.create(course_id=30311, course_name='compsci', description='Computer Science',
                                             semester='Fall')
        self.course2 = Course.objects.create(course_id=30312, course_name='math', description='Mathematics',
                                             semester='Spring')

        # Create days
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
        # Create sections for course1
        self.section1 = Section.objects.create(
            course_parent=self.course1,
            section_id=12301,
            start_time=time(9, 30),
            end_time=time(10, 20),
            type='LEC',
            location= 'None',
            is_online=True
        )
        self.section1.meeting_days.add(self.monday, self.wednesday)
        self.section1.save()

        self.section2=Section.objects.create( course_parent=self.course1,
            section_id=12308,
            start_time= None,
            end_time= None,
            type='DIS',
            location=None,
            is_online=True
        )
        self.section2.save()

        self.section3 = Section.objects.create(
            course_parent=self.course1,
            section_id=12309,
            start_time=time(11, 0),
            end_time=time(12, 30),
            type='LAB',
            location='EMS180',
            is_online=False
        )
        self.section3.meeting_days.add(self.tuesday, self.thursday)
        self.section3.save()

        # Create sections for course2
        self.section4 = Section.objects.create(
            course_parent=self.course2,
            section_id=12310,
            start_time=time(14, 0),
            end_time=time(15, 30),
            type='LEC',
            location='EMS190',
            is_online=False
        )
        self.section4.meeting_days.add(self.monday, self.wednesday)
        self.section4.save()



    def test_section_string_representation(self):
        expected_string1 = f"{self.course1.course_name} LAB 12309 - Days: TU, TH, Time: 11:00 to 12:30, Location: EMS180"
        self.assertEqual(str(self.section3), expected_string1)

        expected_string2 = f"{self.course1.course_name} LEC 12301 - Online"
        self.assertEqual(str(self.section1), expected_string2)

    def test_duplicate_section_creation(self):
        section = SectionClass(course_parent=self.section4.course_parent,
                                           section_id=self.section4.section_id,
                                           meeting_days=self.section4.meeting_days.all(),
                                           location=self.section4.location,
                                           start_time=self.section4.start_time,
                                           end_time=self.section4.end_time,
                                           section_type=self.section4.type,
                                           is_online=self.section4.is_online)
        with self.assertRaises(ValueError):
            section.create_section()

    def test_sectionconstruction_inperson_notime_nodays_nolocation(self):
            with self.assertRaises(ValueError):
                    section=SectionClass(
                    course_parent=self.course1,
                    section_id=12316,
                    start_time=None,
                    end_time=None,
                    section_type='LEC',
                    location=None,
                    is_online=False
                )
                    section.create_section()


    def test_sectionconstruction_inperson_nodays_nolocation(self):
        with self.assertRaises(ValueError):
            section=SectionClass(
                course_parent=self.course1,
                section_id=12317,
                start_time=time(11, 0),
                end_time=time(12, 0),
                section_type='LEC',
                is_online=False
            )
            section.create_section()

    def test_section_inperson_notime(self):
        with self.assertRaises(ValueError):
            section=SectionClass(
                course_parent=self.course1, section_id=12319, start_time=None, end_time=None, section_type='LEC',
                location='EMS200',
                is_online=False
            )
            self.section4.meeting_days.set([self.monday, self.wednesday])
            section.create_section()




    def test_sectionconstruction_normal_inperson(self):
        with self.assertRaises(ValueError):
            section = SectionClass(
                course_parent=self.course1,
                section_id=12318,
                start_time=time(11, 0),
                end_time=time(12, 0),
                section_type='LEC',
                location='Room 101',
                is_online=False
            )
            section.create_section()


    def test_sectionconstruction_online_notime_nodays(self):
        with self.assertRaises(ValueError):
            section=SectionClass(
                course_parent=self.course1,
                section_id=12316,
                start_time=None,
                end_time=None,
                section_type='LEC',
                location='EMS200',
                is_online=True
            )
            section.create_section()

    def test_section_creation_database(self):
        section = SectionClass(course_parent=self.course1, section_id=12320, meeting_days=[self.monday, self.wednesday],
                                location='EMS200', start_time=time(10, 0), end_time=time(11, 0), section_type='LEC',
                                is_online=False)
        section.create_section()
        self.assertTrue(Section.objects.filter(section_id=12320).exists())

    def test_section_creation(self):
        self.assertEqual(self.section1.start_time, time(9, 30))
        self.assertEqual(self.section3.is_online, False)
        section= SectionClass(course_parent=self.section4.course_parent, section_id= 12378,
                                  meeting_days=self.section4.meeting_days.all(), start_time=self.section4.start_time,
                                  end_time=self.section4.end_time,location= 'EMS200',
                                  section_type=self.section4.type, is_online=self.section4.is_online)
        self.assertEqual(section.start_time, self.section4.start_time)
        self.assertEqual(section.end_time, self.section4.end_time)
        self.assertEqual(section.is_online, self.section4.is_online)





    def test_section_time_update(self):
        section_update = SectionClass(course_parent=self.section1.course_parent, section_id=self.section1.section_id, meeting_days=self.section1.meeting_days.all(), start_time=self.section1.start_time, end_time=self.section1.end_time,
                                      section_type=self.section1.type, location=self.section1.location, is_online=self.section1.is_online)
        section_update.edit_meeting_time(time(10, 0), time(11, 0))
        section_update.save_updates()
        section_updated = Section.objects.get(section_id=self.section1.section_id)
        self.assertEqual(section_updated.start_time, time(10, 0))



    def test_delete_section(self):
        section_delete = SectionClass(course_parent=self.section1.course_parent, section_id=self.section1.section_id, meeting_days=self.section1.meeting_days.all(),
                                   location=self.section1.location, start_time=self.section1.start_time, end_time=self.section1.end_time,
                                      section_type=self.section1.type, is_online=self.section1.is_online)
        section_delete.delete_section()
        with self.assertRaises(Section.DoesNotExist):
            Section.objects.get(section_id=section_delete.section_id)

    def test_section_edit(self):
        with self.assertRaises(ValueError):
            initial_section = SectionClass(
                course_parent=self.course1,
                section_id=12345,
                start_time=time(9, 0),
                end_time=time(10, 0),
                section_type='LEC',
                location='Original Location',
                is_online=False
            )
            initial_section.meeting_days.add(self.monday, self.tuesday)

            section_edit = SectionClass(
                course_parent=initial_section.course_parent,
                section_id=initial_section.section_id,
                meeting_days=initial_section.meeting_days.all(),
                start_time=initial_section.start_time,
                end_time=initial_section.end_time,
                section_type=initial_section.type,
                location=initial_section.location,
                is_online=initial_section.is_online
            )
            # Edit section
            result = section_edit.edit_section(old_section_id=initial_section.section_id)

            # Check if edit was reported as successful
            self.assertTrue(result, "Edit function did not return True.")

            # Verify the changes
            updated_section = Section.objects.get(section_id=initial_section.section_id)
            self.assertTrue(updated_section.course_parent, self.course2)
            self.assertEqual(updated_section.start_time, time(10, 0))
            self.assertEqual(updated_section.end_time, time(11, 0))
            self.assertEqual(updated_section.type, 'DIS')
            self.assertEqual(updated_section.location, 'EMS180')
            self.assertFalse(updated_section.is_online)
            updated_days = list(updated_section.meeting_days.all())
            self.assertIn(self.monday, updated_days)
            self.assertIn(self.wednesday, updated_days)
            self.assertNotIn(self.tuesday, updated_days)