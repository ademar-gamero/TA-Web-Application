from classes.UserClass import UserClass
from classes.Account import Account
from classes.Course import Course
from classes.Section import Section


class Admin(UserClass):

    def create_user(self, username, password, name, role, email, phone_number="", address=""):
        Account.create_user(username, password, name, role, email, phone_number, address)

    def delete_user(self, user_id):
        Account.delete_user(user_id)

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

    def edit_user(self, user_id, username=None, password=None, name=None, role=None, email=None, phone=None, address=None):
        Account.edit_user(user_id, username, password, name, role, email, phone, address)

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
