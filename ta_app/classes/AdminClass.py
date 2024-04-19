from ta_app.classes.UserClass import UserClass


class Admin(UserClass):

    def create_user(self, username, password, name, role, email, phone_number, address):
        pass

    def delete_user(self, user_id):
        pass

    def create_course(self, course_id, course_name, description):
        pass

    def create_section(self, course_id, section_id, meeting_time, section_type):
        pass

    def assign_instructor(self, user_id, section_id):
        pass

    def unassign_instructor(self, user_id, section_id):
        pass

    def assign_ta(self, user_id, section_id):
        pass

    def unassign_ta(self, user_id, section_id):
        pass

    def edit_user(self, username, password, name, role, email, phone, address):
        pass

    def edit_course(self, course_id, course_name, description):
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
