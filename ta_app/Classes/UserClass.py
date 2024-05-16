from abc import ABC

import ta_app
from ta_app.models import User, Roles, Section

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models.query import QuerySet

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

        if not isinstance(assigned_sections, list) and not isinstance(assigned_sections, QuerySet):
            all_assigned_sections = assigned_sections.all()
            assigned_sections = all_assigned_sections
        if assigned_sections is not None:
            if isinstance(assigned_sections, Section):
                self.assigned_sections.append(assigned_sections)
            elif isinstance(assigned_sections, QuerySet):
                if assigned_sections.exists():
                    self.assigned_sections = []
                if assigned_sections.count() == 0:
                    self.assigned_sections = []
                for section in assigned_sections:
                    if not isinstance(section, Section):
                        raise ValueError("Invalid Section type")
                    self.assigned_sections.append(section)
            elif isinstance(assigned_sections, list):
                if len(assigned_sections) == 0:
                    self.assigned_sections = []
                for section in assigned_sections:
                    if not isinstance(section, Section):
                        raise ValueError("Invalid Section type")
                    self.assigned_sections.append(section)
            else:
                raise ValueError("Invalid Section type")
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
            User.objects.filter(username=self.username).update(assigned=self.assigned)
        else:
            raise ValueError("Assignment must be a boolean")

    def add_section(self, new_section, user=None):
        assigner = None
        if user is not None:
            assigner = User.objects.get(pk=user)
        if assigner is not None:
            if assigner.role == "Instructor":
                try:
                    assigner.assigned_section.get(course_parent=new_section.course_parent, type="LEC")
                except Section.DoesNotExist:
                    raise ValueError("You are not assigned to the course of the section you are trying to assign.")
        should_assign = False
        if isinstance(new_section, Section):
            if self.role == "Teacher-Assistant" and new_section.type == "LAB":
                try:
                    new_section.assigned_users.get(role="Teacher-Assistant")
                    raise ValueError(self.__str__() + " cannot be assigned, There is already an teacher assistant assigned to this section, " + new_section.__str__())
                except User.DoesNotExist:
                    lecture = (User.objects.get(username=self.username).assigned_section.filter
                            (course_parent=new_section.course_parent, type="LEC"))
                    if lecture:
                        should_assign = True
                    else:
                        raise ValueError(self.__str__() + " cannot be assigned, User is not assigned to a corresponding lecture section in this course")
            elif self.role == "Instructor":
                if new_section.type == "lecture" or new_section.type == "LEC":
                    try:
                        new_section.assigned_users.get(role="Instructor")
                        raise ValueError(self.__str__() + " cannot be assigned, There is already an instructor assigned to this lecture, " +  new_section.__str__())
                    except User.DoesNotExist:
                        should_assign = True
                else:
                    raise ValueError(self.__str__() + " cannot be assigned because Instructors cannot be assigned to lab sections, " + new_section.__str__())
            if self.assigned_sections is None:
                self.assigned_sections = [new_section]
            else:
                if self.assigned_sections.count(new_section) > 0:
                    if new_section.type == "lecture" or new_section.type=="LEC" and (self.role == "Teacher-Assistant"):
                        raise ValueError(self.__str__() + " cannot be assigned, teacher assistant is already assigned to course " + new_section.course_parent.__str__())
                    raise ValueError(self.__str__() + " cannot be assigned, user is already assigned to section " + new_section.__str__())
                if self.assigned:

                    self.check_conflicts(new_section)
                else:
                    if should_assign:
                        self.set_assigned(True)
                self.assigned_sections.append(new_section)
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
                    User.objects.get(username=self.username).assigned_section.remove(section_to_remove)
                    unassigned = True
                    if self.role == "Instructor":
                        for user in section_to_remove.assigned_users.filter(role="Teacher-Assistant", assigned=True):
                            ta = UserClass(username=user.username, password=user.password, name=user.name,
                                           role=user.role, email=user.email, phone_number=user.phone_number,
                                           address=user.address, skills=user.skills,
                                           assigned_sections=list(user.assigned_section.all()), assigned=user.assigned)
                            sections = Section.objects.filter(course_parent=section_to_remove.course_parent,
                                                              assigned_users=user, type="LAB")
                            for section in sections:
                                ta.remove_section(section)
                        if self.assigned_sections:
                            unassigned = False
                    elif self.role == "Teacher-Assistant":
                        if section_to_remove.type == "LEC":
                            to_remove = (User.objects.get(username=self.username).assigned_section.filter
                                         (course_parent=section_to_remove.course_parent))
                            for section in to_remove:
                                self.remove_section(section)
                        for section in self.assigned_sections:
                            if section.type == "LAB":
                                unassigned = False
                                break
                    if unassigned:
                        self.set_assigned(False)
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
        try:
            return User.objects.get(username=self.username).username
        except User.DoesNotExist:
            return self.username

    def get_password(self):
        try:
            return User.objects.get(username=self.username).password
        except User.DoesNotExist:
            return self.password

    def get_name(self):
        try:
            return User.objects.get(username=self.username).name
        except User.DoesNotExist:
            return self.name

    def get_role(self):
        try:
            return User.objects.get(username=self.username).role
        except User.DoesNotExist:
            return self.role

    def get_email(self):
        try:
            return User.objects.get(username=self.username).email
        except User.DoesNotExist:
            return self.email

    def get_phone_number(self):
        try:
            return User.objects.get(username=self.username).phone_number
        except User.DoesNotExist:
            return self.phone_number

    def get_address(self):
        try:
            return User.objects.get(username=self.username).address
        except User.DoesNotExist:
            return self.address

    def get_assigned(self):
        try:
            return User.objects.get(username=self.username).assigned
        except User.DoesNotExist:
            return self.assigned

    def get_assigned_sections(self):
        try:
            return list(User.objects.get(username=self.username).assigned_section.all())
        except User.DoesNotExist:
            return self.assigned_sections

    def get_skills(self):
        try:
            return User.objects.get(username=self.username).skills
        except User.DoesNotExist:
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

    def edit_user(self, username=None, password=None, name=None, role=None, email=None, phone=None, address=None,
                  skills=None):
        old_username = self.username

        if username is not None:
            try:
                User.objects.get(username=username)
                raise ValueError("Username already in use. Please choose a unique username.")
            except User.DoesNotExist or ValueError as e:
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
                                       role=self.get_role(), email=self.get_email(),
                                       phone_number=self.get_phone_number(),
                                       address=self.get_address(), assigned=self.get_assigned(),skills=self.get_skills())
            for i in self.assigned_sections:
                user.assigned_section.add(i)
            user.save()

    def delete_user(self):
        try:
            val_to_del = User.objects.get(username=self.get_username())
            if self.role == "Instructor":
                for section in self.assigned_sections:
                    self.remove_section(section)
            val_to_del.delete()
            return True
        except User.DoesNotExist:
            raise ValueError("This user does not exist and can not be deleted")

    def check_conflicts(self, new_section):
        possible_conflict = False
        if self.role == "Teacher-Assistant" and new_section.type == "LEC":
            return
        for section in self.assigned_sections:
            for day1 in section.meeting_days.values_list():
                for day2 in new_section.meeting_days.values_list():
                    if day1 == day2:
                        possible_conflict = True
                if possible_conflict:
                    if self.role == "Teacher-Assistant" and section.type == "LEC":
                        continue
                    conflict = True
                    if new_section.start_time < section.start_time:
                        if new_section.end_time < section.start_time:
                            conflict = False
                    if new_section.start_time > section.end_time:
                        conflict = False
                    if conflict:
                        days = []
                        for day in new_section.meeting_days.values_list('day',flat=True):
                            days.append(day)
                        raise ValueError("The section being assigned conflicts with another section assignment : " + section.__str__() + f" - {days} - {section.start_time.strftime("%H:%M")} to {section.end_time.strftime("%H:%M")}")
                possible_conflict = False
