
from ta_app.models import Section, Course, Day
from datetime import time

class SectionClass:
    def __init__(self, course_parent=None, section_id=None,meeting_days=None, start_time=None, end_time=None,
                 section_type=None, location=None, is_online=False):

        if not isinstance(course_parent, Course):
            raise ValueError("course_parent must be an instance of Course")
        if course_parent is None:
            raise ValueError("course_parent must not be None")

        self.course_parent = course_parent
        self.section_id = section_id
        self.section_type = section_type
        self.meeting_days = meeting_days
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.is_online = is_online

    def create_section(self):
        if Section.objects.filter(course_parent=self.course_parent, section_id=self.section_id,
                                  start_time=self.start_time, end_time=self.end_time,
                                  type=self.section_type).exists():
            raise ValueError("Duplicate section exists.")
        section = Section.objects.create(course_parent=self.course_parent, section_id=self.section_id,
                                         start_time=self.start_time, end_time=self.end_time,
                                         type=self.section_type, is_online=self.is_online)
        if not self.is_online:
            for day in self.meeting_days:
                section.meeting_days.add(day)
        return True



    def edit_meeting_days(self, new_days):
        if not self.is_online:
            self.meeting_days = new_days

    def add_meeting_days(self, new_days):
        if not self.is_online:
            self.meeting_days.extend(new_days)

    def remove_meeting_days(self, day):
        if not self.is_online:
            self.meeting_days.remove(day)

    def edit_meeting_time(self, new_start_time, new_end_time):
        self.start_time = new_start_time
        self.end_time = new_end_time

    def edit_type(self, new_type):
        self.section_type = new_type

    def edit_course_parent(self, new_course):
        self.course_parent = new_course

    def save_updates(self):
        Section.objects.filter(id=self.section_id).update(
            course_parent=self.course_parent,
            section_id=self.section_id,
            meeting_days=self.meeting_days,
            start_time=self.start_time,
            end_time=self.end_time,
            type=self.section_type,
            location=self.location,
            is_online=self.is_online
        )
    def delete_section(self):
        section = Section.objects.get(id=self.section_id)
        section.delete()
        return True
