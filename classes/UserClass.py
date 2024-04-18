from abc import ABC
from ta_app.models import User, Roles, Section


class UserClass(ABC):

    def __init__(self, username, password, name, role, email, phone_number="", address=""):
        self.username = username
        self.password = password
        self.name = name
        self.role = role
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.assigned = False
        self.assigned_sections = None

    def __str__(self):
        return f'{self.name} : {self.role}'

    def set_password(self, new_password):
        pass

    def set_username(self, new_username):
        pass

    def set_email(self, new_email):
        pass

    def set_phone_number(self, new_phone):
        pass

    def set_address(self, new_address):
        pass

    def set_name(self, new_name):
        pass

    def set_role(self, new_role):
        pass

    def set_assigned(self, new_assigned):
        pass

    def add_section(self, new_section):
        pass

    def remove_section(self, section_to_remove):
        pass

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_name(self):
        return self.name

    def get_role(self):
        return self.role

    def get_email(self):
        return self.email

    def get_phone_number(self):
        return self.phone_number

    def get_address(self):
        return self.address

    def get_assigned(self):
        return self.assigned

    def get_assigned_sections(self):
        return self.assigned_sections

    def set_contact_info(self, email, phone_number, address):
        pass

    def get_contact_info(self, user_id):
        pass
