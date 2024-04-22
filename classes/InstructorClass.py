from ta_app.models import Section, Roles
import UserClass
class Instructor(UserClass):
    def __init__(self, username, password, name, email, phone_number="", address=""):
        super().__init__(username, password, name, Roles.INSTRUCTOR, email, phone_number, address)
        self.assigned_sections = []

    def set_contact_info(self, email, phone_number, address):
        self.email = email
        self.phone_number = phone_number
        self.address = address

    def assign_TA_to_section(self):
        pass