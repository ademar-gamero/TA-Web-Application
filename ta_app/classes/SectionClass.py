from ta_app.models import Section
from datetime import datetime


class SectionClass:
    def __init__(self, course_parent, section_id, meeting_time, section_type):
        self.course_parent = course_parent
        self.section_id = section_id
        self.meeting_time = meeting_time
        self.section_type = section_type

    def __str__(self):
        return f"{self.course_parent.course_name} {self.section_type} {self.section_id}"

    def create_section(self):
        # Creates a section instance using the instance attributes
        section = Section.objects.create(
            course_parent=self.course_parent,
            section_id=self.section_id,
            meeting_time=self.meeting_time,
            type=self.section_type
        )
        section.save()
        return section

    def edit_section_id(self, new_id):
        self.section_id = new_id
        self.save()

    def edit_meeting_time(self, new_time):
        self.meeting_time = new_time
        self.save()

    def edit_type(self, new_type):
        self.section_type = new_type
        self.save()

    def edit_course_parent(self, new_course):
        self.course_parent = new_course
        self.save()

    def delete_section(self):
        section = Section.objects.get(id=self.section_id)
        section.delete()
        return section