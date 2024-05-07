from abc import ABC

from ta_app.models import User, Roles, Section

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


from abc import ABC

from ta_app.models import User, Roles, Section
from django.core.validators import validate_email


class UserClass(ABC):

    def __init__(self, username, password, name, role, email, phone_number="", address="", assigned=False,
                 assigned_sections=None, skills=""):
        if (username == "" or password == "" or name == "" or role == "" or email == ""
                or username is None or password is None or name is None or role is None or email is None):
            raise ValueError("Must include username, password, name, role, and email.")
        if not isinstance(username, str) or username.strip() == "":
            raise ValueError("Username must be a non-empty string")
        if not isinstance(password, str) or password.strip() == "":
            raise ValueError("Password must be a non-empty string")
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non-empty string")
        if username.replace(" ", "") != username:
            raise ValueError("Username cannot contain spaces")
        if password.replace(" ", "") != password:
            raise ValueError("Password cannot contain spaces")

        if not (role == "Teacher-Assistant" or role == "Instructor" or role == "Admin"):
            raise ValueError("Invalid role")
        if not isinstance(phone_number, str):
            raise ValueError("Invalid phone number")
        if not isinstance(address, str):
            raise ValueError("Invalid phone number")
        if not isinstance(assigned, bool):
            raise ValueError("Assigned must be a boolean")
        if not isinstance(skills, str):
            raise ValueError("Skills must be a string")
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Email is not valid")

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
        self.skills = skills

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

            self.username = new_username

        else:
            raise ValueError("New Username must not be None")

    def set_email(self, new_email):
        try:
            validate_email(new_email)
        except ValidationError:
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
            if not (new_role == "Teacher-Assistant" or new_role == "Instructor" or new_role == "Admin"):

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
                if self.assigned:
                    # checks for conflicts if user already assigned. if it finds one, this will throw an error
                    self.check_conflicts(new_section)
                self.assigned_sections.append(new_section)
            if self.role == "Teacher-Assistant" and new_section.type == "LAB":
                lecture = (User.objects.get(username=self.username).assigned_section.filter
                           (course_parent=new_section.course_parent, type="LEC"))
                if lecture:
                    self.set_assigned(True)
                else:
                    raise ValueError("User is not assigned to a corresponding lecture section in this course")
            elif self.role == "Instructor":
                if new_section.type == "LEC":
                    self.set_assigned(True)
                else:
                    raise ValueError("Instructors cannot be assigned to lab sections")
            User.objects.get(username=self.username).assigned_section.add(new_section)
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

    def set_skills(self, new_skills):
        if isinstance(new_skills, str):
            self.skills = new_skills
        else:
            raise ValueError("Skills must be a string")

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

    def get_skills(self):
        return self.skills

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

    def edit_user(self, username=None, password=None, name=None, role=None, email=None, phone=None, address=None, skills=None):
        old_username = self.username

        if username is not None:
            try: 
                User.objects.get(username=username)
                raise ValueError("Username already in use. Please choose a unique username.")
            except User.DoesNotExist:
                self.set_username(username)
        if password is not None:
            self.set_password(password)
        if name is not None:
            self.set_name(name)
        if role is not None:
            self.set_role(role)
        if email is not None:
            try: 
                User.objects.get(email=email)
                raise ValueError("Email already in use. Please use a unique email.")
            except User.DoesNotExist:
                self.set_email(email)
        if phone is not None:
            try:
                User.objects.get(phone_number=phone)
            except User.DoesNotExist:
                self.set_phone_number(phone)
        if address is not None:
            self.set_address(address)
        if skills is not None:
            self.set_skills(skills)
        User.objects.filter(username=old_username).update(username=self.username, password=self.password,
                                                          name=self.name,
                                                          role=self.role, email=self.email,
                                                          phone_number=self.phone_number,
                                                          address=self.address, skills=self.skills)

    def create_user(self):
        try:
            User.objects.get(username=self.username)
            raise ValueError("Username is already taken")
        except User.DoesNotExist:
            user = User.objects.create(username=self.get_username(), password=self.get_password(), name=self.get_name(),
                        role=self.get_role(), email=self.get_email(), phone_number=self.get_phone_number(),
                        address=self.get_address(),assigned=self.get_assigned(), skills=self.get_skills())
            for i in self.assigned_sections:
                user.assigned_section.add(i)
            user.save()

    def delete_user(self):
        try:
            val_to_del = User.objects.get(username=self.get_username())
            val_to_del.delete()
            return True
        except User.DoesNotExist:
            raise ValueError("This user does not exist can not be deleted")
    
    def check_conflicts(self, new_section):
        possible_conflict = False
        for section in self.assigned_sections:
            for day1 in section.meeting_days:
                for day2 in new_section.meeting_days:
                    if day1 == day2:
                        possible_conflict = True
                if possible_conflict:
                    if new_section.start_time >= section.start_time and new_section.end_time <= section.end_time:
                        raise ValueError("The section being assigned conflicts with another section assignment :"
                                         + section.__str__())
                possible_conflict = False



