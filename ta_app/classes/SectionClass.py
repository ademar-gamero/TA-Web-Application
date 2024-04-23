from ta_app.models import Section, Course
from datetime import datetime
class SectionClass:
    def __init__(self, course_parent=None, section_id=None, meeting_time=None, section_type=None):
        if not isinstance(course_parent, Course):
            raise ValueError("course_parent must be an instance of Course")
        if course_parent is None:
            raise ValueError("course_parent must be not None")
        self.course_parent = course_parent
        self.section_id = section_id
        self.meeting_time = meeting_time
        self.section_type = section_type

    def create_section(self):
        # Check for duplicates before creating a new section
        if Section.objects.filter(course_parent=self.course_parent, section_id=self.section_id, meeting_time=self.meeting_time, type=self.section_type).exists():
            raise ValueError("Duplicate section exists.")
        Section.objects.create(
            course_parent=self.course_parent,
            section_id=self.section_id,
            meeting_time=self.meeting_time,
            type=self.section_type  # Ensuring it maps to 'type', not 'section_type'
        )
        return True
    def edit_section_id(self, new_id):
        self.section_id = new_id

    def edit_meeting_time(self, new_time):
        self.meeting_time = new_time

    def edit_type(self, new_type):
        self.section_type = new_type

    def edit_course_parent(self, new_course):
        self.course_parent = new_course

    def save_updates(self):
        # This method updates the section in the database with current instance values
        Section.objects.filter(id=self.section_id).update(
            course_parent=self.course_parent,
            section_id=self.section_id,
            meeting_time=self.meeting_time,
            type=self.section_type
        )

    def delete_section(self):
        section = Section.objects.get(id=self.section_id)
        section.delete()
        return True
