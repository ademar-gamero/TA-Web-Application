from ta_app.classes.UserClass import UserClass
from classes.Course import Course
from classes.Section import Section


class Admin(UserClass):

    def create_course(self, course_id, course_name, description=""):
        CourseClass.create_course(course_id, course_name, description)

    def create_section(self, course_id, section_id, meeting_time, section_type):
        SectionClass.create_section(course_id, section_id, meeting_time, section_type)

    def assign_instructor(self, user_id, section_id):
        SectionClass.assign_instructor(user_id, section_id)

    def unassign_instructor(self, user_id, section_id):
        SectionClass.unassign_instructor(user_id,section_id)

    def assign_ta(self, user_id, section_id):
        SectionClass.assign_ta(user_id, section_id)

    def unassign_ta(self, user_id, section_id):
        SectionClass.unassign_ta(user_id, section_id)

    def edit_course(self, course_id, course_name=None, description=None):
        CourseClass.edit_course(course_id, course_name, description)

    def delete_course(self, course_id):
        Course.delete_course(course_id)

    def edit_section(self, course_id, section_id, meeting_time=None, section_type=None):
        Section.edit_section(course_id, section_id, meeting_time, section_type)

    def delete_section(self, course_id, section_id):
        Section.delete_section(course_id, section_id)

    def message_all(self, message):
        pass
