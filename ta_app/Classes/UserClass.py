from abc import ABC

from django.core.exceptions import ValidationError

from ta_app.models import User, Roles, Section
from django.core.validators import validate_email


class UserClass:

    def __init__(self, username="", password="", name="", role="", email="", phone_number="", address="", assigned=False,
                 assigned_sections=None):
        if username == "" or password == "" or name == "" or role == "" or email == "":
            raise ValueError("Must include username, password, name, role, and email.")
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError("Username must not be empty")
        if not isinstance(password, str) or password.strip() == "":
            raise ValueError("Password must not be empty")
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must not be empty")
        if username.strip() != username:
            raise ValueError("Username cannot contain spaces")
        if password.strip() != password:
            raise ValueError("Password cannot contain spaces")
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email address")
        if not (role == "Teacher-Assistant" or role == "Instructor" or role == "Admin"):
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
        self.assigned_sections = []
        if assigned_sections is not None:
            self.assigned_sections = assigned_sections

    def __str__(self):
        return f'{self.name} : {self.role}'

    def set_password(self, new_password):
        if new_password is not None:
            if not isinstance(new_password, str):
                raise ValueError("New Password must be a string")
            if new_password.strip() == "":
                raise ValueError("New Password must not be empty")
            self.password = new_password
        else:
            raise ValueError("New Password must not be None")

    def set_username(self, new_username):
        if new_username is not None:
            if not isinstance(new_username, str):
                raise ValueError("New Username must be a string")
            if new_username.strip() == "":
                raise ValueError("New Username must not be empty")
            try:
                User.objects.get(username=new_username)
                raise ValueError("Username is already taken")
            except User.DoesNotExist:
                self.password = new_username
        else:
            raise ValueError("New Username must not be None")

    def set_email(self, new_email):
        if not validate_email(new_email):
            raise ValueError("Email is not valid")
        self.email = new_email

    def set_phone_number(self, new_phone):
        if isinstance(new_phone, str):
            self.phone_number = new_phone
        else:
            raise ValueError("New Phone number must be a string")

    def set_address(self, new_address):
        if isinstance(new_address, str):
            self.address = new_address
        else:
            raise ValueError("New Address must be a string")

    def set_name(self, new_name):
        if isinstance(new_name, str):
            if new_name.strip() == "":
                raise ValueError("New Name cannot be empty")
            self.name = new_name
        else:
            raise ValueError("New Name must be a string")

    def set_role(self, new_role):
        if isinstance(new_role, str):
            if not (new_role is "Teacher-Assistant" or new_role is "Instructor" or new_role is "Admin"):
                raise ValueError("Invalid role")
            self.role = new_role
        else:
            raise ValueError("Invalid role")

    def set_assigned(self, new_assigned):
        if isinstance(new_assigned, bool):
            self.assigned = new_assigned
        else:
            raise ValueError("Assignment must be a boolean")

    def add_section(self, new_section):
        if isinstance(new_section, Section):
            if self.assigned_sections is None:
                self.assigned_sections = [new_section]
            else:
                if self.assigned_sections.count(new_section) > 0:
                    raise ValueError("User is already assigned to this section")
                self.assigned_sections.append(new_section)
        else:
            raise ValueError("Invalid section entry")

    def remove_section(self, section_to_remove):
        if isinstance(section_to_remove, Section):
            if self.assigned_sections is None:
                raise ValueError("Section not in user's assigned sections")
            else:
                try:
                    self.assigned_sections.remove(section_to_remove)
                except ValueError:
                    raise ValueError("Section not in user's assigned sections")
        else:
            raise ValueError("Invalid section entry")

    def view_contact_info(self, username):
        if not isinstance(username, str):
            raise ValueError("Invalid username")
        try:
            contact = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("User does not exist")
        if self.role == "Admin":
            return contact.email, contact.phone_number, contact.address
        else:
            return contact.email

    def edit_user(self, username=None, password=None, name=None, role=None, email=None, phone=None, address=None):
        old_username = self.username
        if username is not None and username != self.username:
            self.set_username(username)
        if password is not None and password != self.password:
            self.set_password(password)
        if name is not None and name != self.name:
            self.set_name(name)
        if role is not None and role != self.role:
            self.set_role(role)
        if email is not None and email != self.email:
            self.set_email(email)
        if phone is not None and phone != self.phone_number:
            self.set_phone_number(phone)
        if address is not None and address != self.address:
            self.set_address(address)
        User.objects.filter(username=old_username).update(username=self.username, password=self.password,
                                                          name=self.name,
                                                          role=self.role, email=self.email,
                                                          phone_number=self.phone_number,
                                                          address=self.address)

    def create_user(self):
        try:
            User.objects.get(username=self.username)
            raise ValueError("Username is already taken")
        except User.DoesNotExist:
            user = User(username=self.username, password=self.password, name=self.name,
                        role=self.role(), email=self.email, phone=self.phone_number,
                        address=self.address)
            user.save()

    def delete_user(self):
        User.objects.filter(username=self.username).delete()
