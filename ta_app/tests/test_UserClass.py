from django.test import TestCase
from ta_app.Classes.UserClass import UserClass
from ta_app.models import Course, Section, User, Day
from datetime import datetime, time


class Common(TestCase):
    def setUp(self):
        date_string = "Wed 2:30pm"
        date_object = datetime.strptime(date_string, "%a %H:%M%p")
        date_string = "Tue 2:30pm"
        date_object2 = datetime.strptime(date_string, "%a %H:%M%p")
        date_string = "Fri 2:30pm"
        date_object3 = datetime.strptime(date_string, "%a %H:%M%p")
        self.admin = User(name="ad", username="admin", password="admin", email="admin@email.com", role="Admin",
                          phone_number=1, address="1", assigned=False)
        self.admin.save()
        self.algos = Course(course_id=351, course_name="compsci", description="blah blah blah")
        self.algos.save()
        self.section = Section(course_parent=self.algos, section_id=12345, type="lecture")
        self.section.save()
        self.section2 = Section(course_parent=self.algos, section_id=123478, type="lab")
        self.section2.save()
        print(self.section2)
        slist1 = [self.section]
        slist2 = [self.section, self.section2]
        self.section3 = Section(course_parent=self.algos, section_id=1234789, type="lab")
        self.section3.save()
        self.assigned_user0 = UserClass("ta", "ta", "apoorv", "Teacher-Assistant", "email@gmail.com", "1", "1", True,
                                        slist1)
        self.assigned_user = UserClass("ta", "ta", "apoorv", "Teacher-Assistant", "email@email.com", "1", "1", True,
                                       slist2)


class setPass(Common):
    def test_setpass(self):
        with self.assertRaises(ValueError, msg="New Password must be a string"):
            self.assigned_user.set_password(123)

    def test_setpassCorrect(self):
        self.assigned_user.set_password("password")
        self.assertEqual("password", self.assigned_user.password)


class setUser(Common):
    def test_setuser(self):
        with self.assertRaises(ValueError, msg="New Username must be a string"):
            self.assigned_user.set_username(123)

    def test_setpassCorrect(self):
        self.assigned_user.set_username("password")
        self.assertEqual("password", self.assigned_user.username)


class setEmail(Common):
    def test_setEmail(self):
        with self.assertRaises(ValueError, msg="Email is not valid"):
            self.assigned_user.set_email("emaileamil.com")

    def test_setEmailCorrect(self):
        self.assigned_user.set_email("email@freemail.com")
        self.assertEqual("email@freemail.com", self.assigned_user.email)


class set_phone_number(Common):
    def test_setPhone(self):
        with self.assertRaises(ValueError, msg="New Phone number must be a string"):
            self.assigned_user.set_phone_number(123)

    def test_setPhoneCorrect(self):
        self.assigned_user.set_phone_number("414-777-777")
        self.assertEqual("414-777-777", self.assigned_user.phone_number)


class set_address(Common):
    def test_setAdress(self):
        with self.assertRaises(ValueError, msg="New Address number must be a string"):
            self.assigned_user.set_address(123)

    def test_setPhoneCorrect(self):
        self.assigned_user.set_address("7th street")
        self.assertEqual("7th street", self.assigned_user.address)


class set_name(Common):
    def test_setName(self):
        with self.assertRaises(ValueError, msg="New Name number must be a string"):
            self.assigned_user.set_name(123)

    def test_setPhoneCorrect(self):
        self.assigned_user.set_name("adam")
        self.assertEqual("adam", self.assigned_user.name)


class set_role(Common):
    def test_setRole(self):
        with self.assertRaises(ValueError, msg="New Phone number must be a string"):
            self.assigned_user.set_role("President")

    def test_setPhoneCorrect(self):
        self.assigned_user.set_role("Teacher-Assistant")
        self.assertEqual("Teacher-Assistant", self.assigned_user.role)


class set_assigned(Common):
    def test_setAssigned(self):
        with self.assertRaises(ValueError, msg="Assignment must be a boolean"):
            self.assigned_user.set_assigned("President")

    def test_setAssignedCorrect(self):
        self.assigned_user.set_assigned(True)
        self.assertEqual(True, self.assigned_user.assigned)


class set_skills(Common):
    def test_setSkills(self):
        with self.assertRaises(ValueError, msg="Skills must be a string"):
            self.assigned_user.set_skills(True)

    def test_setSkillsCorrect(self):
        self.assigned_user.set_skills("CS 361")
        self.assertEqual("CS 361", self.assigned_user.skills)


class TestUserClass(Common):

    def test_createNullAll(self):
        with self.assertRaises(TypeError, msg="Fails to catch invalid entry"):
            temp = UserClass()

    # shouldn't be able to create a user with no name, password, etc

    def test_createNullUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid username"):
            temp = UserClass(None, "pass", "name", "TA", "email@email.com")

    # shouldn't be able to create a user with a null username

    def test_createNullPassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid password"):
            temp = UserClass("username", None, "name", "TA", "email@email.com")

    # shouldn't be able to create a user with a null password

    def test_createNullName(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid name"):
            temp = UserClass("username", "pass", None, "TA", "email@email.com")

    # shouldn't be able to create a user with a null name

    def test_createNullRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid role"):
            temp = UserClass("username", "pass", "name", None, "email@email.com")

    # shouldn't be able to create a user with a null role

    def test_createNullEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid email"):
            temp = UserClass("username", "pass", "name", "TA", None)

    # shouldn't be able to create a user with a null email

    def test_createEmptyUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            temp = UserClass("", "pass", "name", "TA", "email@email.com")

    # shouldn't be able to create a user with an empty username

    def test_createEmptyPassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            temp = UserClass("username", "", "name", "TA", "email@email.com")

    # shouldn't be able to create a user with an empty password

    def test_createEmptyName(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            temp = UserClass("username", "pass", "", "TA", "email@email.com")

    # shouldn't be able to create a user with an empty name

    def test_createEmptyRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty role"):
            temp = UserClass("username", "pass", "name", "", "email@email.com")

    # shouldn't be able to create a user with an empty role

    def test_createEmptyEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty email"):
            temp = UserClass("username", "pass", "name", "TA", "")

    # shouldn't be able to create a user with an empty email

    def test_createWhitespaceUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            temp = UserClass(" ", "pass", "name", "TA", "email@email.com")

    # shouldn't be able to create a user with an empty username

    def test_createWhitespacePassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            temp = UserClass("username", "  ", "name", "TA", "email@email.com")

    # shouldn't be able to create a user with an empty password

    def test_createWhitespaceName(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            temp = UserClass("username", "pass", "   ", "TA", "email@email.com")

    # shouldn't be able to create a user with an empty name

    def test_createWhitespaceRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty role"):
            temp = UserClass("username", "pass", "name", " ", "email@email.com")

    # shouldn't be able to create a user with an empty role

    def test_createWhitespaceEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty email"):
            temp = UserClass("username", "pass", "name", "TA", "  ")

    # shouldn't be able to create a user with an empty email

    def test_createBadEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch bad email"):
            temp = UserClass("username", "pass", "name", "TA", "randomwords")

    # shouldn't be able to create a user with a bad email (no @something.something)

    def test_createBadRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch bad role"):
            temp = UserClass("username", "pass", "name", "Batman", "email@email.com")

    def test_createAdmin(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Admin")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Admin", "Role is wrong")
        self.assertEqual(temp.phone_number, "", "Phone number should be empty")
        self.assertEqual(temp.address, "", "Address should be empty")
        self.assertEqual(temp.assigned, False, "Should not be assigned")

        self.assertEqual(temp.assigned_sections, [], "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : Admin", "toString returns incorrectly")

    # check if creating an Admin with all necessary inputs returns successfully

    def test_createInstructor(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Instructor")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Instructor", "Role is wrong")
        self.assertEqual(temp.phone_number, "", "Phone number should be empty")
        self.assertEqual(temp.address, "", "Address should be empty")
        self.assertEqual(temp.assigned, False, "Should not be assigned")

        self.assertEqual(temp.assigned_sections, [], "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : Instructor", "toString returns incorrectly")

    # check if creating an Instructor with all necessary inputs returns successfully

    def test_createTA(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Teacher-Assistant")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Teacher-Assistant", "Role is wrong")
        self.assertEqual(temp.phone_number, "", "Phone number should be empty")
        self.assertEqual(temp.address, "", "Address should be empty")
        self.assertEqual(temp.assigned, False, "Should not be assigned")
        self.assertEqual(temp.assigned_sections, [], "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : Teacher-Assistant", "toString returns incorrectly")

    # check if creating a TA with all necessary inputs returns successfully

    def test_createWithDetails(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Admin",

                         phone_number="123-4567", address="123 Fake Street")

        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Admin", "Role is wrong")
        self.assertEqual(temp.phone_number, "123-4567", "Phone number is wrong")
        self.assertEqual(temp.address, "123 Fake Street", "Address is wrong")
        self.assertEqual(temp.assigned, False, "Should not be assigned")

        self.assertEqual(temp.assigned_sections, [], "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : Admin", "toString returns incorrectly")
    # check if creating a user with additional details (phone/address) returns successfully


class create_User(TestCase):
    def test_createToDB(self):
        date_string = "Tue 2:30pm"
        date_object = datetime.strptime(date_string, "%a %H:%M%p")
        algos = Course(course_id=351, course_name="compsci", description="blah blah blah")
        algos.save()

        section = Section(course_parent=algos, section_id=12345, type="lecture")
        section.save()

        slist = [section]
        self.assigned_user = UserClass("ta", "ta", "apoorv", "Teacher-Assistant", "email@email.com", "1", "1", True,
                                       slist)
        self.assigned_user.create_user()
        db_user = User.objects.get(name="apoorv")

        self.assertEqual(db_user.username, self.assigned_user.username, "Username is wrong")
        self.assertEqual(db_user.password, self.assigned_user.password, "Password is wrong")
        self.assertEqual(db_user.name, self.assigned_user.name, "Name is wrong")
        self.assertEqual(db_user.role, self.assigned_user.role, "Role is wrong")
        self.assertEqual(db_user.email, self.assigned_user.email, "Email is wrong")
        self.assertEqual(db_user.phone_number, self.assigned_user.phone_number, "Phone is wrong")
        self.assertEqual(db_user.address, self.assigned_user.address, "Address is wrong")
        self.assertEqual(db_user.assigned, True, "Assigned is incorrect")
        j = 0
        for i in db_user.assigned_section.all():
            self.assertEqual(self.assigned_user.assigned_sections[j], i, "assigned sections not present")
            j = j + 1


class TestEditUser(TestCase):

    def setUp(self):
        self.user = UserClass(username='user', password='password', name="Name", role="Admin", email="bla@bla.com",

                              phone_number="1234567890", address="Home", assigned=False)
        self.user.create_user()
        self.user2 = UserClass(username='user2', password='password2', name="Name2", role="Admin",
                               email="bla@blast.com", phone_number="123", address="Apartment", assigned=False)
        self.user2.create_user()

    def test_edit_user_duplicate_username(self):
        with self.assertRaises(ValueError, msg="Username already exists"):
            self.user.edit_user("user2", None, None, None, None, None, None)
        self.assertEqual("user", self.user.username, msg="Username was updated when it shouldnt have been")
        count = User.objects.filter(username=self.user.username).count()
        print(count)
        self.assertTrue(count == 1, "Username was updated in the db, when it shouldnt have been")

    def test_edit_user_duplicate_email(self):
        self.user.edit_user(None, None, None, None, None, None, self.user2.email)
        self.assertEqual("bla@bla.com", self.user.email, msg="Email was updated when it shouldnt have been")
        count = User.objects.filter(email=self.user.email).count()
        self.assertTrue(count == 1, "Username was updated in the db, when it shouldnt have been")

    def test_edit_user_duplicate_phoneNumber(self):
        self.user.edit_user(None, None, None, None, None, self.user2.phone_number, None)
        self.assertEqual("1234567890", self.user.phone_number,
                         msg="Phone number was updated when it shouldnt have been")
        count = User.objects.filter(phone_number=self.user.phone_number).count()
        self.assertTrue(count == 1, "Username was updated in the db, when it shouldnt have been")

    def test_edit_user_username(self):
        self.user.edit_user("new", None, None, None, None, None, None)
        self.assertEqual("new", self.user.username, msg="Username was not updated")
        self.assertTrue(User.objects.filter(username=self.user.username).exists(),
                        "Username wasn't updated in the db")
        check = User.objects.get(username=self.user.username)
        self.assertEqual("password", check.password, "Password should not have changed")
        self.assertEqual("Name", check.name, "Name should not have changed")

        self.assertEqual("Admin", check.role, "Role should have changed")
        self.assertEqual("bla@bla.com", check.email, "Email should not have changed")
        self.assertEqual("1234567890", check.phone_number, "Phone number should not have changed")
        self.assertEqual("Home", check.address, "Address should not have changed")

    def test_edit_user_password(self):
        self.user.edit_user(None, "newpass", None, None, None, None, None)
        self.assertEqual("newpass", self.user.password, msg="Password was not updated")
        check = User.objects.get(username="user")
        self.assertEqual(self.user.password, check.password, "Password was not changed")

        self.assertEqual("Name", check.name, "Name should not have changed")

        self.assertEqual("Admin", check.role, "Role should have changed")
        self.assertEqual("bla@bla.com", check.email, "Email should not have changed")
        self.assertEqual("1234567890", check.phone_number, "Phone number should not have changed")
        self.assertEqual("Home", check.address, "Address should not have changed")

    def test_edit_user_name(self):
        self.user.edit_user(None, None, "New Name", None, None, None, None)
        self.assertEqual("New Name", self.user.name, msg="Name was not updated")
        check = User.objects.get(username="user")

        self.assertEqual("password", check.password, "Password should not have changed")

        self.assertEqual("New Name", check.name, "Name should have changed")
        self.assertEqual("Admin", check.role, "Role should not have changed")
        self.assertEqual("bla@bla.com", check.email, "Email should not have changed")
        self.assertEqual("1234567890", check.phone_number, "Phone number should not have changed")
        self.assertEqual("Home", check.address, "Address should not have changed")

    def test_edit_user_role(self):
        self.user.edit_user(None, None, None, "Instructor", None, None, None)
        self.assertEqual("Instructor", self.user.role, msg="Role was not updated")
        check = User.objects.get(username="user")

        self.assertEqual("password", check.password, "Password should not have changed")

        self.assertEqual("Name", check.name, "Name should not have changed")
        self.assertEqual("Instructor", check.role, "Role should have changed")
        self.assertEqual("bla@bla.com", check.email, "Email should not have changed")
        self.assertEqual("1234567890", check.phone_number, "Phone number should not have changed")
        self.assertEqual("Home", check.address, "Address should not have changed")

    def test_edit_user_email(self):
        self.user.edit_user(None, None, None, None, "new@aol.com", None, None)
        self.assertEqual("new@aol.com", self.user.email, msg="Email was not updated")
        check = User.objects.get(username="user")

        self.assertEqual("password", check.password, "Password should not have changed")

        self.assertEqual("Name", check.name, "Name should not have changed")
        self.assertEqual("Admin", check.role, "Role should not have changed")
        self.assertEqual("new@aol.com", check.email, "Email should have changed")
        self.assertEqual("1234567890", check.phone_number, "Phone number should not have changed")
        self.assertEqual("Home", check.address, "Address should not have changed")

    def test_edit_user_phone(self):
        self.user.edit_user(None, None, None, None, None, "555-5555", None)
        self.assertEqual("555-5555", self.user.phone_number, msg="Phone was not updated")
        check = User.objects.get(username="user")

        self.assertEqual("password", check.password, "Password should not have changed")

        self.assertEqual("Name", check.name, "Name should not have changed")
        self.assertEqual("Admin", check.role, "Role should not have changed")
        self.assertEqual("bla@bla.com", check.email, "Email should not have changed")
        self.assertEqual("555-5555", check.phone_number, "Phone number should have changed")
        self.assertEqual("Home", check.address, "Address should not have changed")

    def test_edit_user_address(self):
        self.user.edit_user(None, None, None, None, None, None, "The Moon")
        self.assertEqual("The Moon", self.user.address, msg="Address was not updated")
        check = User.objects.get(username="user")

        self.assertEqual("password", check.password, "Password should not have changed")

        self.assertEqual("Name", check.name, "Name should not have changed")
        self.assertEqual("Admin", check.role, "Role should not have changed")
        self.assertEqual("bla@bla.com", check.email, "Email should not have changed")
        self.assertEqual("1234567890", check.phone_number, "Phone number should not have changed")
        self.assertEqual("The Moon", check.address, "Address should have changed")

    def test_edit_user_all(self):
        self.user.edit_user("new", "newpass", "New Name", "Instructor", "new@aol.com",
                            "555-5555", "The Moon")
        self.assertEqual("new", self.user.username, msg="Username was not updated")
        self.assertEqual("newpass", self.user.password, msg="Password was not updated")
        self.assertEqual("New Name", self.user.name, msg="Name was not updated")
        self.assertEqual("Instructor", self.user.role, msg="Role was not updated")
        self.assertEqual("new@aol.com", self.user.email, msg="Email was not updated")
        self.assertEqual("555-5555", self.user.phone_number, msg="Phone was not updated")
        self.assertEqual("The Moon", self.user.address, msg="Address was not updated")
        self.assertTrue(User.objects.filter(username="new").exists(), "Username wasn't updated in the db")
        check = User.objects.get(username="new")

        self.assertEqual("newpass", self.user.password, "Password should have changed")

        self.assertEqual("New Name", check.name, "Name should have changed")
        self.assertEqual("Instructor", check.role, "Role should have changed")
        self.assertEqual("new@aol.com", check.email, "Email should have changed")
        self.assertEqual("555-5555", check.phone_number, "Phone number should have changed")
        self.assertEqual("The Moon", check.address, "Address should have changed")

    def test_edit_user_usernameBad(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid username"):
            self.user.edit_user(True, None, None, None, None, None, None)

    def test_edit_user_passwordBad(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid password"):
            self.user.edit_user(None, " ", None, None, None, None, None)

    def test_edit_user_nameBad(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid name"):
            self.user.edit_user(None, None, 123, None, None, None, None)

    def test_edit_user_roleBad(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid role"):
            self.user.edit_user(None, None, None, "Bear", None, None, None)

    def test_edit_user_emailBad(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid email"):
            self.user.edit_user(None, None, None, None, "None", None, None)

    def test_edit_user_phoneBad(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid phone number"):
            self.user.edit_user(None, None, None, None, None, [1, 2, 3], None)

    def test_edit_user_addressBad(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid address"):
            self.user.edit_user(None, None, None, None, None, None, 200.2)


class SectionAssignmentTests(TestCase):

    def setUp(self):
        self.monday = Day.objects.create(day="MO")
        self.tuesday = Day.objects.create(day="TU")
        self.wednesday = Day.objects.create(day="WE")
        self.thursday = Day.objects.create(day="TH")
        self.friday = Day.objects.create(day="FR")
        self.ta = UserClass(username="test_ta", password="pass", name="TA Man", role="Teacher-Assistant",
                            email="ta@uwm.edu")
        self.ta.create_user()
        self.instructor = UserClass(username="test_in", password="pass", name="Instructo", role="Instructor",
                                    email="in@uwm.edu")
        self.instructor.create_user()
        self.course1 = Course.objects.create(course_id=101, course_name="Math", description="blah", semester="Fall")
        self.lecture1 = Section.objects.create(course_parent=self.course1, section_id=100, type="LEC",
                                               start_time=time(12, 0), end_time=time(13, 30), location="who cares")
        self.lecture1.meeting_days.add(self.monday, self.wednesday)
        self.lecture2 = Section.objects.create(course_parent=self.course1, section_id=101, type="LEC",
                                               start_time=time(12, 0), end_time=time(13, 30))
        self.lecture2.meeting_days.add(self.tuesday, self.thursday)
        self.lecture3 = Section.objects.create(course_parent=self.course1, section_id=102, type="LEC",
                                               start_time=time(11, 0), end_time=time(12, 30))
        self.lecture3.meeting_days.add(self.monday, self.wednesday)
        self.lecture4 = Section.objects.create(course_parent=self.course1, section_id=103, type="LEC",
                                               start_time=time(9, 0), end_time=time(10, 30))
        self.lecture4.meeting_days.add(self.tuesday, self.thursday)
        self.lab1 = Section.objects.create(course_parent=self.course1, section_id=300, type="LAB",
                                           start_time=time(12, 0), end_time=time(13, 30))
        self.lab1.meeting_days.add(self.monday, self.wednesday)
        self.lab2 = Section.objects.create(course_parent=self.course1, section_id=400, type="LAB",
                                           start_time=time(9, 0), end_time=time(10, 30))
        self.lab2.meeting_days.add(self.monday, self.wednesday)
        self.lab3 = Section.objects.create(course_parent=self.course1, section_id=500, type="LAB",
                                           start_time=time(9, 0), end_time=time(10, 30))
        self.lab3.meeting_days.add(self.tuesday, self.thursday)
        self.lab4 = Section.objects.create(course_parent=self.course1, section_id=600, type="LAB",
                                           start_time=time(10, 00), end_time=time(11, 30))
        self.lab4.meeting_days.add(self.monday, self.friday)

    def test_assignInstructorSingle(self):
        self.instructor.add_section(self.lecture1)
        self.assertEqual(self.instructor.assigned_sections[0], self.lecture1, "Lecture 1 should be assigned")
        self.assertTrue(self.instructor.assigned, "Assigned flag not set for instructor")

    def test_assignInstructorLab(self):
        self.instructor.add_section(self.lecture1)
        self.assertEqual(self.instructor.assigned_sections[0], self.lecture1, "Lecture 1 should be assigned")
        self.assertTrue(self.instructor.assigned, "Assigned flag not set for instructor")
        with self.assertRaises(ValueError, msg="Lab shouldn't be assignable to instructor"):
            self.instructor.add_section(self.lab1)

    def test_assignInstructorNoConflictDifferentDays(self):
        self.instructor.add_section(self.lecture1)
        self.instructor.add_section(self.lecture2)
        self.assertEqual(self.instructor.assigned_sections[0], self.lecture1, "Section 1 should be assigned")
        self.assertEqual(self.instructor.assigned_sections[1], self.lecture2, "Section 2 should be assigned")
        self.assertTrue(self.instructor.assigned, "Assigned flag not set for instructor")

    def test_assignInstructorNoConflictSameDays(self):
        self.instructor.add_section(self.lecture2)
        self.instructor.add_section(self.lecture4)
        self.assertEqual(self.instructor.assigned_sections[0], self.lecture2, "Section 1 should be assigned")
        self.assertEqual(self.instructor.assigned_sections[1], self.lecture4, "Section 2 should be assigned")
        self.assertTrue(self.instructor.assigned, "Assigned flag not set for instructor")

    def test_assignInstructorConflict(self):
        self.instructor.add_section(self.lecture1)
        with self.assertRaises(ValueError, msg="Did not catch conflicting times"):
            self.instructor.add_section(self.lecture3)

    def test_assignTaNoLecture(self):
        with self.assertRaises(ValueError, msg="Did not catch lack of required lecture assignment before lab assigned"):
            self.ta.add_section(self.lab1)

    def test_assignTaLecture(self):
        self.ta.add_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections[0], self.lecture1, "Lecture 1 should be assigned")
        self.assertFalse(self.ta.assigned, "Assigned flag should not be set for TA with only lectures")

    def test_assignTaToLab(self):
        self.ta.add_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections[0], self.lecture1, "Lecture 1 should be assigned")
        self.assertFalse(self.ta.assigned, "Assigned flag should not be set for TA with only lectures")
        self.ta.add_section(self.lab1)
        self.assertEqual(self.ta.assigned_sections[1], self.lab1, "Lab 1 wasn't added successfully")
        self.assertTrue(self.ta.assigned, "Assigned flag should be set for TA when they have a lab section")

    def test_assignTaToLabsNoConflictDifferentDays(self):
        self.ta.add_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections[0], self.lecture1, "Lecture 1 should be assigned")
        self.assertFalse(self.ta.assigned, "Assigned flag should not be set for TA with only lectures")
        self.ta.add_section(self.lab1)
        self.assertEqual(self.ta.assigned_sections[1], self.lab1, "Lab 1 wasn't added successfully")
        self.assertTrue(self.ta.assigned, "Assigned flag should be set for TA when they have a lab section")
        self.ta.add_section(self.lab3)
        self.assertEqual(self.ta.assigned_sections[2], self.lab3, "Lab wasn't added successfully")

    def test_assignTALectureAndLabNonConflict(self):
        self.ta.add_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections[0], self.lecture1, "Lecture 1 should be assigned")
        self.assertFalse(self.ta.assigned, "Assigned flag should not be set for TA with only lectures")
        self.ta.add_section(self.lab2)
        self.assertEqual(self.ta.assigned_sections[1], self.lab2, "Lab 2 wasn't added successfully")
        self.assertTrue(self.ta.assigned, "Assigned flag should be set for TA when they have a lab section")
        self.ta.add_section(self.lab1)
        self.assertEqual(self.ta.assigned_sections[2], self.lab1, "Lab 1 wasn't added successfully")

    def test_assignTAMeultipleLecturesNoActualConflict(self):
        self.ta.add_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections[0], self.lecture1, "Lecture 1 should be assigned")
        self.assertFalse(self.ta.assigned, "Assigned flag should not be set for TA with only lectures")
        self.ta.add_section(self.lab2)
        self.assertEqual(self.ta.assigned_sections[1], self.lab2, "Lab 2 wasn't added successfully")
        self.assertTrue(self.ta.assigned, "Assigned flag should be set for TA when they have a lab section")
        self.ta.add_section(self.lecture3)
        self.assertEqual(self.ta.assigned_sections[2], self.lecture3, "Lecture 3 wasn't added successfully")

    def test_assignTAMultipleLabLectureNoActualConflict(self):
        self.ta.add_section(self.lecture3)
        self.assertEqual(self.ta.assigned_sections[0], self.lecture3, "Lecture 3 should be assigned")
        self.assertFalse(self.ta.assigned, "Assigned flag should not be set for TA with only lectures")
        self.ta.add_section(self.lab1)
        self.assertEqual(self.ta.assigned_sections[1], self.lab1, "Lab 1 wasn't added successfully")
        self.assertTrue(self.ta.assigned, "Assigned flag should be set for TA when they have a lab section")
        self.ta.add_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections[2], self.lecture1, "Lecture 1 wasn't added successfully")

    def test_assignTwoInstructors(self):
        self.instructor2 = UserClass(username="test_in2", password="pass", name="Instructor Two", role="Instructor",
                                    email="in2@uwm.edu")
        self.instructor2.create_user()
        self.instructor.add_section(self.lecture2)
        with self.assertRaises(ValueError, msg="Failed to stop second instructor from being assigned to same section"):
            self.instructor2.add_section(self.lecture2)


class RemoveSectionTests(TestCase):

    def setUp(self):
        self.monday = Day.objects.create(day="MO")
        self.tuesday = Day.objects.create(day="TU")
        self.wednesday = Day.objects.create(day="WE")
        self.thursday = Day.objects.create(day="TH")
        self.friday = Day.objects.create(day="FR")
        self.ta = UserClass(username="test_ta", password="pass", name="TA Man", role="Teacher-Assistant",
                            email="ta@uwm.edu")
        self.ta.create_user()
        self.instructor = UserClass(username="test_in", password="pass", name="Instructo", role="Instructor",
                                    email="in@uwm.edu")
        self.instructor.create_user()
        self.course1 = Course.objects.create(course_id=101, course_name="Math", description="blah", semester="Fall")
        self.course2 = Course.objects.create(course_id=401, course_name="Super Math", description="blah",
                                             semester="Fall")
        self.lecture1 = Section.objects.create(course_parent=self.course1, section_id=100, type="LEC",
                                               start_time=time(12, 0), end_time=time(13, 30), location="who cares")
        self.lecture1.meeting_days.add(self.monday, self.wednesday)
        self.lecture2 = Section.objects.create(course_parent=self.course2, section_id=101, type="LEC",
                                               start_time=time(12, 0), end_time=time(13, 30))
        self.lecture2.meeting_days.add(self.tuesday, self.thursday)
        self.lecture3 = Section.objects.create(course_parent=self.course1, section_id=102, type="LEC",
                                               start_time=time(11, 0), end_time=time(12, 30))
        self.lecture3.meeting_days.add(self.monday, self.wednesday)
        self.lab1 = Section.objects.create(course_parent=self.course1, section_id=300, type="LAB",
                                           start_time=time(12, 0), end_time=time(13, 30))
        self.lab1.meeting_days.add(self.monday, self.wednesday)
        self.lab2 = Section.objects.create(course_parent=self.course1, section_id=400, type="LAB",
                                           start_time=time(9, 0), end_time=time(10, 30))
        self.lab2.meeting_days.add(self.tuesday, self.thursday)
        self.lab3 = Section.objects.create(course_parent=self.course2, section_id=500, type="LAB",
                                           start_time=time(16, 0), end_time=time(17, 30))
        self.lab3.meeting_days.add(self.tuesday, self.thursday)
        self.instructor.add_section(self.lecture1)
        self.instructor.add_section(self.lecture2)
        self.ta.add_section(self.lecture1)
        self.ta.add_section(self.lab1)
        self.ta.add_section(self.lab2)

    def test_removeTALab(self):
        self.ta.remove_section(self.lab1)
        self.assertEqual(self.ta.assigned_sections[1], self.lab2, "Lab 1 wasn't removed successfully")
        self.assertTrue(self.ta.assigned, "TA should still be assigned")

    def test_removeTAAllLabs(self):
        self.ta.remove_section(self.lab1)
        self.assertEqual(self.ta.assigned_sections[1], self.lab2, "Lab 1 wasn't removed successfully")
        self.assertTrue(self.ta.assigned, "TA should still be assigned")
        self.ta.remove_section(self.lab2)
        self.assertEqual(len(self.ta.assigned_sections), 1, "Lab 2 wasn't removed successfully")
        self.assertFalse(self.ta.assigned, "TA should not be assigned")

    def test_removeTALec(self):
        self.ta.remove_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections, [], "Lecture and all associated labs should be removed")
        self.assertFalse(self.ta.assigned, "TA should not be assigned")

    def test_removeTAInvalid(self):
        with self.assertRaises(ValueError, msg="Invalid section not caught"):
            self.ta.remove_section(self.lab3)

    def test_removeTAWithMultipleCourses(self):
        self.ta.add_section(self.lecture2)
        self.ta.add_section(self.lab3)
        self.ta.remove_section(self.lecture1)
        self.assertEqual(self.ta.assigned_sections[0], self.lecture2, "Lecture 1 and its labs should be removed")
        self.assertEqual(self.ta.assigned_sections[1], self.lab3, "Lecture 1 and its labs should be removed")
        self.assertTrue(self.ta.assigned, "TA should still be assigned")

    def test_removeInstructor(self):
        self.instructor.remove_section(self.lecture1)
        self.assertEqual(self.instructor.assigned_sections[0], self.lecture2, "Lecture 1 should be removed")
        self.assertTrue(self.instructor.assigned, "Instructor should still be assigned")
        # this next bit checks if TAs get unassigned from LAB sections tied to the instructor's LEC.
        # commented out as I'm not sure if we want it to work this way or not
        self.assertEqual(len(self.ta.get_assigned_sections()), 1,
                         "Instructor's removal from lecture should take TA out of associated labs")
        self.assertFalse(self.ta.get_assigned(), "Instructor's removal should unassign TA if not assigned elsewhere")

    def test_removeInstructorFromAll(self):
        self.instructor.remove_section(self.lecture1)
        self.assertEqual(self.instructor.assigned_sections[0], self.lecture2, "Lecture 1 should be removed")
        self.assertTrue(self.instructor.assigned, "Instructor should still be assigned")
        self.instructor.remove_section(self.lecture2)
        self.assertEqual(self.instructor.assigned_sections, [], "Lecture 2 should be removed")
        self.assertFalse(self.instructor.assigned, "Instructor should not be assigned")

    def test_removeInstructorInvalid(self):
        with self.assertRaises(ValueError, msg="Invalid section not caught"):
            self.instructor.remove_section(self.lecture3)
