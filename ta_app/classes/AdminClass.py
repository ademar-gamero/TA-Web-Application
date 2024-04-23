from ta_app.Classes.UserClass import UserClass
from ta_app.Classes.CourseClass import Course
from ta_app.Classes.SectionClass import Section


class Admin(UserClass):

    def create_course(self, course_id, course_name, description=""):
        Course.create_course(course_id, course_name, description)

    def create_section(self, course_id, section_id, meeting_time, section_type):
        Section.create_section(course_id, section_id, meeting_time, section_type)

    def assign_instructor(self, user_id, section_id):
        Section.assign_instructor(user_id, section_id)

    def unassign_instructor(self, user_id, section_id):
        Section.unassign_instructor(user_id,section_id)

    def assign_ta(self, user_id, section_id):
        Section.assign_ta(user_id, section_id)

    def unassign_ta(self, user_id, section_id):
        Section.unassign_ta(user_id, section_id)

    def edit_course(self, course_id, course_name=None, description=None):
        Course.edit_course(course_id, course_name, description)

    def delete_course(self, course_id):
        Course.delete_course(course_id)

    def edit_section(self, course_id, section_id, meeting_time=None, section_type=None):
        Section.edit_section(course_id, section_id, meeting_time, section_type)

    def delete_section(self, course_id, section_id):
        Section.delete_section(course_id, section_id)

    def message_all(self, message):
        pass
