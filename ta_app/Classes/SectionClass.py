from django.core.exceptions import ValidationError
from django.db import models
from datetime import time, datetime

from ta_app.models import Section, Course,Day


class SectionClass:

    def __init__(self, course_parent=None, section_id=None, meeting_days=None, start_time=None, end_time=None,
                 section_type=None, location=None, is_online=None):
        if course_parent is None:
            raise ValueError("course_parent must not be None")
        if not isinstance(course_parent, Course):
            raise ValueError("course_parent must be an instance of Course")

        if start_time is not None and not isinstance(start_time, time) :

                start_time = datetime.strptime(start_time, '%H:%M').time()

        if end_time is not None and not isinstance(end_time, time) :

                end_time = datetime.strptime(end_time, '%H:%M').time()

        if start_time is not None and end_time is not None:
            if start_time == end_time:
                raise ValueError("Start time and end time must not be the same")
            if start_time > end_time:
                raise ValueError("Start time must be before end time")
        if not isinstance(is_online, bool):
            raise ValueError("is_online must be a boolean")
        if not is_online:
            if location =='None':
                raise ValueError("Location must be provided for in-person classes")
            if meeting_days is None:
                raise ValueError("Meeting days must be provided for in-person classes")
            if start_time is None or end_time is None:
                raise ValueError("Start time and end time must be provided for in-person classes")
        if is_online:
            if location !='None':
                raise ValueError("Please enter 'None' in location for online classes")
        if location is not 'None' :
            #start time   is in between the start and end time of another section
            if Section.objects.filter(location=location, start_time__range=[start_time, end_time]).exists():
                raise ValueError("Section in the same location and at same time can not be added.")
        self.course_parent = course_parent
        if section_id is None:
            raise ValueError("Section ID must not be None")
        self.section_id = section_id
        self.meeting_days = []
        if meeting_days is not None:
            for day in meeting_days:
                if not isinstance(day, Day):
                    raise ValueError("meeting_days must be a list of Day objects")
                self.meeting_days.append(day)
        self.start_time = start_time
        self.end_time = end_time
        self.section_type = section_type
        self.location = location
        self.is_online = is_online

    def create_section(self):
        if Section.objects.filter(section_id=self.section_id).exists():
            raise ValueError("Duplicate section exists.")
        for day in self.meeting_days:
            if Section.objects.filter(location=self.location, start_time=self.start_time,
                                      end_time=self.end_time, meeting_days__in=[day]).exists():
                raise ValueError("Section in the same location and at same time can not be added.")
        section = Section.objects.create(
            course_parent=self.course_parent,
            section_id=self.section_id,
            start_time=self.start_time,
            end_time=self.end_time,
            type=self.section_type,
            location=self.location,
            is_online=self.is_online
        )
        for day in self.meeting_days:
            section.meeting_days.add(day)
        section.save()
        return True

    def save_updates(self):
        try:
            section = Section.objects.get(section_id=self.section_id)
        except Section.DoesNotExist:
            raise ValidationError("Section does not exist")

        section.start_time = self.start_time
        section.end_time = self.end_time
        section.type = self.section_type
        section.location = self.location
        section.is_online = self.is_online
        section.save()

        if not self.is_online:
            section.meeting_days.set(
                self.meeting_days)

    def edit_meeting_time(self, new_start_time, new_end_time):
        self.start_time = new_start_time
        self.end_time = new_end_time

    def edit_type(self, new_type):
        self.section_type = new_type

    def edit_course_parent(self, new_course):
        self.course_parent = new_course

    def delete_section(self):
        section = Section.objects.get(section_id=self.section_id)
        section.delete()
        return True

    def edit_section(self, old_section_id):
        old_section= Section.objects.get(section_id=old_section_id)
        for day in self.meeting_days:
            if old_section.section_id!=self.section_id and old_section.location != self.location and old_section.start_time != self.start_time and old_section.end_time != self.end_time:
                if Section.objects.filter(location=self.location, start_time=self.start_time,
                                          end_time=self.end_time, meeting_days__in=[day]).exists():
                    obj=Section.objects.get(location=self.location, start_time=self.start_time,
                                          end_time=self.end_time, meeting_days__in=[day])
                    raise ValueError(f"The section being edited conflicts with another section assignment :{self.course_parent} {self.section_type} {obj.section_id} {self.location} {self.start_time} to {self.end_time} ")
        section = Section.objects.get(section_id=old_section_id)
        section.course_parent = self.course_parent
        section.section_id = self.section_id
        section.start_time = self.start_time
        section.end_time = self.end_time
        section.type = self.section_type
        section.location = self.location
        section.is_online = self.is_online
        section.meeting_days.set(self.meeting_days)
        section.save()
