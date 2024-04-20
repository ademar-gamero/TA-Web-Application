from classes.UserClass import UserClass


class Admin(UserClass):

    def create_user(self, username, password, name, role, email, phone_number=None, address=None):
        pass

    def delete_user(self, user_id):
        pass

    def create_course(self, course_id, course_name, description=None):
        pass

    def create_section(self, course_id, section_id, meeting_time, section_type):
        pass

    def assign_instructor(self, user, section_id):
        pass

    def unassign_instructor(self, user, section_id):
        pass

    def assign_ta(self, user, section_id):
        pass

    def unassign_ta(self, user, section_id):
        pass

    def edit_user(self, user, username=None, password=None, name=None, role=None, email=None, phone=None, address=None):
        pass

    def edit_course(self, course_id, course_name=None, description=None):
        pass

    def delete_course(self, course_id):
        pass

    def edit_section(self, course_id, section_id, meeting_time, section_type):
        pass

    def delete_section(self, section_id):
        pass

    def message_all(self, message):
        pass

    # Override
    def get_contact_info(self, user_id):
        pass
