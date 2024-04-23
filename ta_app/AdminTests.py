from django.test import TestCase
from ta_app.classes.AdminClass import Admin


class TestAdminClass(TestCase):
    ad = None

    def setUp(self):
        self.ad = Admin("admin", "admin", "Admin", "AD", "admin@admin.com")

    def test_createUserTA(self):
        user = self.ad.create_user("newuser", "password", "NewTA", "TA", "email@uwm.edu")
        self.assertEqual("newuser", user.username, "Username is wrong")
        self.assertEqual("password", user.password, "Password is wrong")
        self.assertEqual("NewTA", user.name, "Name is wrong")
        self.assertEqual("TA", user.role, "Role is wrong")
        self.assertEqual("email@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("", user.phone_number, "Phone is wrong")
        self.assertEqual("", user.address, "Address is wrong")
        self.assertFalse(user.assigned, "Should not be assigned upon creation")
        self.assertEqual(None, user.assigned_sections, "Should not be in any sections upon creation")

    def test_createUserInstructor(self):
        user = self.ad.create_user("newuser", "password", "NewIN", "IN", "email@uwm.edu")
        self.assertEqual("newuser", user.username, "Username is wrong")
        self.assertEqual("password", user.password, "Password is wrong")
        self.assertEqual("NewIN", user.name, "Name is wrong")
        self.assertEqual("IN", user.role, "Role is wrong")
        self.assertEqual("email@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("", user.phone_number, "Phone is wrong")
        self.assertEqual("", user.address, "Address is wrong")
        self.assertFalse(user.assigned, "Should not be assigned upon creation")
        self.assertEqual(None, user.assigned_sections, "Should not be in any sections upon creation")

    def test_createUserAdmin(self):
        user = self.ad.create_user("newuser", "password", "NewAD", "AD", "email@uwm.edu")
        self.assertEqual("newuser", user.username, "Username is wrong")
        self.assertEqual("password", user.password, "Password is wrong")
        self.assertEqual("NewAD", user.name, "Name is wrong")
        self.assertEqual("AD", user.role, "Role is wrong")
        self.assertEqual("email@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("", user.phone_number, "Phone is wrong")
        self.assertEqual("", user.address, "Address is wrong")
        self.assertFalse(user.assigned, "Should not be assigned upon creation")
        self.assertEqual(None, user.assigned_sections, "Should not be in any sections upon creation")

    def test_createUserFullDetails(self):
        user = self.ad.create_user("newuser", "password", "New", "IN", "email@uwm.edu",
                                   "555-5555", "123 Fake Street")
        self.assertEqual("newuser", user.username, "Username is wrong")
        self.assertEqual("password", user.password, "Password is wrong")
        self.assertEqual("New", user.name, "Name is wrong")
        self.assertEqual("IN", user.role, "Role is wrong")
        self.assertEqual("email@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("555-5555", user.phone_number, "Phone is wrong")
        self.assertEqual("123 Fake Street", user.address, "Address is wrong")
        self.assertFalse(user.assigned, "Should not be assigned upon creation")
        self.assertEqual(None, user.assigned_sections, "Should not be in any sections upon creation")

    def test_delete_user(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.delete_user(user.get_user_id())
        self.assertEqual(None, user, "User was not deleted")

    def test_delete_userNull(self):
        with self.assertRaises(ValueError, msg="Fails to catch wrong input type"):
            self.ad.delete_user(None)

    def test_delete_userNonUser(self):
        with self.assertRaises(ValueError, msg="Fails to catch wrong input type"):
            self.ad.delete_user("Tacos")

    def test_edit_userFull(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user.get_user_id(), "newUsername", "newPass", "New Name", "IN", "newemail@uwm.edu",
                          "555-5555", "123 Fake Street")
        self.assertEqual("newUsername", user.username, "Username is wrong")
        self.assertEqual("newPass", user.password, "Password is wrong")
        self.assertEqual("New Name", user.name, "Name is wrong")
        self.assertEqual("IN", user.role, "Role is wrong")
        self.assertEqual("newemail@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("555-5555", user.phone_number, "Phone is wrong")
        self.assertEqual("123 Fake Street", user.address, "Address is wrong")

    def test_edit_userUsername(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user.get_user_id(), "newUsername")
        self.assertEqual("newUsername", user.username, "Username is wrong")
        self.assertEqual("password", user.password, "Password is wrong")
        self.assertEqual("New", user.name, "Name is wrong")
        self.assertEqual("TA", user.role, "Role is wrong")
        self.assertEqual("email@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("", user.phone_number, "Phone is wrong")
        self.assertEqual("", user.address, "Address is wrong")

    def test_edit_userUsernameEmpty(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            self.ad.edit_user(user.get_user_id(), "")

    def test_edit_userPassword(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user.get_user_id(), password="newPass")
        self.assertEqual("newuser", user.username, "Username is wrong")
        self.assertEqual("newPass", user.password, "Password is wrong")
        self.assertEqual("New", user.name, "Name is wrong")
        self.assertEqual("TA", user.role, "Role is wrong")
        self.assertEqual("email@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("", user.phone_number, "Phone is wrong")
        self.assertEqual("", user.address, "Address is wrong")

    def test_edit_userPasswordEmpty(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            self.ad.edit_user(user.get_user_id(), password="")

    def test_edit_userName(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user.get_user_id(), name="New Name")
        self.assertEqual("newuser", user.username, "Username is wrong")
        self.assertEqual("password", user.password, "Password is wrong")
        self.assertEqual("New Name", user.name, "Name is wrong")
        self.assertEqual("TA", user.role, "Role is wrong")
        self.assertEqual("email@uwm.edu", user.email, "Email is wrong")
        self.assertEqual("", user.phone_number, "Phone is wrong")
        self.assertEqual("", user.address, "Address is wrong")

    def test_edit_userNameEmpty(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            self.ad.edit_user(user.get_user_id(), name="")

    def test_edit_userNameNonString(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch invalid value type"):
            self.ad.edit_user(user.get_user_id(), name=123)

    def test_create_course(self):
        course = self.ad.create_course(101, "English", "A generic class")

    def test_create_courseNoDescription(self):
        course = self.ad.create_course(101, "English")

    def test_create_courseNull(self):
        with self.assertRaises(ValueError, msg="Fails to catch null input"):
            course = self.ad.create_course(None, None, None)

    def test_create_courseNullID(self):
        with self.assertRaises(ValueError, msg="Fails to catch null input"):
            course = self.ad.create_course(None, "Math", None)

    def test_create_courseEmptyID(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty input"):
            course = self.ad.create_course("", "Math", None)

    def test_create_courseNullName(self):
        with self.assertRaises(ValueError, msg="Fails to catch null input"):
            course = self.ad.create_course(101, None, None)

    def test_create_courseEmptyName(self):
        with self.assertRaises(ValueError, msg="Fails to catch empty input"):
            course = self.ad.create_course(101, "", None)

    def test_edit_course(self):
        course = self.ad.create_course(101, "English")
        self.ad.edit_course(101, "Math", "A basic math class")

    def test_delete_course(self):
        course = self.ad.create_course(101, "English")
        self.ad.delete_course(101)

    def test_create_section(self):
        course = self.ad.create_course(101, "English")
        section = self.ad.create_section(101, 555, "M 5:30", "LAB")

    def test_edit_section(self):
        pass

    def test_delete_section(self):
        pass

    def test_assign_instructor(self):
        pass

    def test_assign_instructor_null(self):
        pass

    def test_assign_instructor_duplicate(self):
        pass

    def test_assign_instructor_conflicting_section(self):
        pass

    def test_assign_ta(self):
        pass

    def test_assign_ta_null(self):
        pass

    def test_assign_ta_duplicate(self):
        pass

    def test_assign_ta_conflicting_section(self):
        pass

    def test_unassign_instructor(self):
        pass

    def test_unassign_instructor_null(self):
        pass

    def test_unassign_instructor_no_section(self):
        pass

    def test_unnassign_instructor_not_assigned(self):
        pass
