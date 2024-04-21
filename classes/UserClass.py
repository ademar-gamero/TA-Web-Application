from abc import ABC
from ta_app.models import User, Roles, Section
from django.core.validators import validate_email


class UserClass(ABC):

    def __init__(self, username, password, name, role, email, phone_number="", address="", assigned=False,
                 assigned_sections=None):
        if username is None or password is None or name is None or role is None or email is None:
            raise ValueError("Missing necessary parameters. Must include username, password, name, role, and email.")
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError("Username must be a non-empty string")
        if not isinstance(password, str) or password.strip() == "":
            raise ValueError("Password must be a non-empty string")
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string")
        if username.strip() != username:
            raise ValueError("Username cannot contain spaces")
        if password.strip() != password:
            raise ValueError("Password cannot contain spaces")
        if not validate_email(email):
            raise ValueError("Email is not valid")
        if not (role is "TA" or role is "IN" or role is "AD"):
            raise ValueError("Invalid role")
        if not isinstance(phone_number, str):
            raise ValueError("Invalid phone number")
        if not isinstance(address, str):
            raise ValueError("Invalid phone number")
        if not isinstance(assigned, bool):
            raise ValueError("Assigned must be a boolean")
        if assigned_sections is not None:
            if isinstance(assigned_sections, list):
                for section in assigned_sections:
                    if not isinstance(section, int):
                        raise ValueError("Assigned Sections must be listed by their ID")
            else:
                raise ValueError("Assigned Sections must be listed by their ID")
        self.username = username
        self.password = password
        self.name = name
        self.role = role
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.assigned = assigned
        self.assigned_sections = assigned_sections
        self.user = User(self.username, self.password, self.name, self.role, self.email, self.phone_number, self.address,
                    self.assigned, self.assigned_sections)
        self.user.save()
        self.user_id = self.user.id

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

    def get_user_id(self):
        return self.user_id

    def set_contact_info(self, email, phone_number, address):
        pass

    def get_contact_info(self, user_id):
        pass
