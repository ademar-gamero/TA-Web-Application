from django.test import TestCase
from classes.UserClass import UserClass
from ta_app.models import User, Section, Course


class TestUserClass(TestCase):

    def setUp(self):
        self.user = UserClass(username='user', password='password', name="Name", role="Admin", email="bla@bla.com")

    def test_createNullAll(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid entry"):
            temp = UserClass(None, None, None, None, None)
    # shouldn't be able to create a user with no name, password, etc

    def test_createNullUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid username"):
            temp = UserClass(None, "pass", "name", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with a null username

    def test_createNullPassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid password"):
            temp = UserClass("username", None, "name", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with a null password

    def test_createNullName(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid name"):
            temp = UserClass("username", "pass", None, "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with a null name

    def test_createNullRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid role"):
            temp = UserClass("username", "pass", "name", None, "email@email.com")
    # shouldn't be able to create a user with a null role

    def test_createNullEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch invalid email"):
            temp = UserClass("username", "pass", "name", "Teacher's-Assistant", None)
    # shouldn't be able to create a user with a null email

    def test_createEmptyUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            temp = UserClass("", "pass", "name", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with an empty username

    def test_createEmptyPassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            temp = UserClass("username", "", "name", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with an empty password

    def test_createEmptyName(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            temp = UserClass("username", "pass", "", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with an empty name

    def test_createEmptyRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty role"):
            temp = UserClass("username", "pass", "name", "", "email@email.com")
    # shouldn't be able to create a user with an empty role

    def test_createEmptyEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty email"):
            temp = UserClass("username", "pass", "name", "Teacher's-Assistant", "")
    # shouldn't be able to create a user with an empty email

    def test_createWhitespaceUsername(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            temp = UserClass(" ", "pass", "name", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with an empty username

    def test_createWhitespacePassword(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            temp = UserClass("username", "  ", "name", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with an empty password

    def test_createWhitespaceName(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            temp = UserClass("username", "pass", "   ", "Teacher's-Assistant", "email@email.com")
    # shouldn't be able to create a user with an empty name

    def test_createWhitespaceRole(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty role"):
            temp = UserClass("username", "pass", "name", " ", "email@email.com")
    # shouldn't be able to create a user with an empty role

    def test_createWhitespaceEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty email"):
            temp = UserClass("username", "pass", "name", "Teacher's-Assistant", "  ")
    # shouldn't be able to create a user with an empty email

    def test_createBadEmail(self):
        with self.assertRaises(ValueError, msg="Fails to catch bad email"):
            temp = UserClass("username", "pass", "name", "Teacher's-Assistant", "randomwords")
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
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : AD", "toString returns incorrectly")
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
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : IN", "toString returns incorrectly")
    # check if creating an Instructor with all necessary inputs returns successfully

    def test_createTA(self):
        temp = UserClass(username="new", password="pass", name="New", email="new@uwm.edu", role="Teacher's-Assistant")
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "pass", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Teacher's-Assistant", "Role is wrong")
        self.assertEqual(temp.phone_number, "", "Phone number should be empty")
        self.assertEqual(temp.address, "", "Address should be empty")
        self.assertEqual(temp.assigned, False, "Should not be assigned")
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : TA", "toString returns incorrectly")
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
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : AD", "toString returns incorrectly")
    # check if creating a user with additional details (phone/address) returns successfully

    def test_createWithBadDetails(self):
        temp = UserClass(username="new", password="password", name="New", email="new@uwm.edu", role="Admin",
                         phone_number=404, address=12.5)
        self.assertEqual(temp.username, "new", "Username is wrong")
        self.assertEqual(temp.password, "password", "Password is wrong")
        self.assertEqual(temp.name, "New", "Name is wrong")
        self.assertEqual(temp.email, "new@uwm.edu", "Email is wrong")
        self.assertEqual(temp.role, "Admin", "Role is wrong")
        self.assertEqual(temp.phone_number, "123-4567", "Phone number is wrong")
        self.assertEqual(temp.address, "123 Fake Street", "Address is wrong")
        self.assertEqual(temp.assigned, False, "Should not be assigned")
        self.assertEqual(temp.assigned_sections, None, "Shouldn't be assigned to any sections")
        self.assertEqual(temp.__str__(), "New : AD", "toString returns incorrectly")
    # check if creating a user with additional details (phone/address) that are faulty will be caught

    def test_edit_username(self):
        self.user.set_username("newname")
        self.assertEqual("newname", self.user.username, "Username not correctly changed")

    def test_edit_password(self):
        self.user.set_password("newpass")
        self.assertEqual("newpass", self.user.password, "Password not correctly changed")

    def test_edit_name(self):
        self.user.set_name("New Name")
        self.assertEqual("New Name", self.user.name, "Name was not correctly changed")

    def test_edit_email(self):
        self.user.set_email("new@uwm.edu")
        self.assertEqual("new@uwm.edu", self.user.email, "Email was not correctly changed")

    def test_edit_role(self):
        self.user.set_role("Instructor")
        self.assertEqual("Instructor", self.user.role, "Role was not correctly changed")

    def test_edit_phone_number(self):
        self.user.set_phone_number("123-456-7890")
        self.assertEqual("123-456-7890", self.user.phone_number, "Phone number was not correctly changed")

    def test_edit_address(self):
        self.user.set_address("The Moon")
        self.assertEqual("The Moon", self.user.address, "Address was not correctly changed")