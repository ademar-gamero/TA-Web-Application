from django.test import TestCase
from classes.AdminClass import Admin


class TestAdminClass(TestCase):
    ad = None

    def setUp(self):
        self.ad = Admin("admin", "admin", "Admin", "AD", "admin@admin.com")

    def test_createUserTA(self):
        user = self.ad.create_user("newuser", "password", "NewTA", "TA", "email@uwm.edu")

    def test_createUserInstructor(self):
        user = self.ad.create_user("newuser", "password", "NewIN", "IN", "email@uwm.edu")

    def test_createUserAdmin(self):
        user = self.ad.create_user("newuser", "password", "NewAD", "AD", "email@uwm.edu")

    def test_createUserFullDetails(self):
        user = self.ad.create_user("newuser", "password", "New", "IN", "email@uwm.edu",
                                   "555-5555", "123 Fake Street")

    def test_delete_user(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.delete_user(user)

    def test_delete_userNull(self):
        with self.assertRaises(ValueError, msg="Fails to catch wrong input type"):
            self.ad.delete_user(None)

    def test_delete_userNonUser(self):
        with self.assertRaises(ValueError, msg="Fails to catch wrong input type"):
            self.ad.delete_user("Tacos")

    def test_edit_userFull(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user, "newUsername", "newPass", "New Name", "IN", "newemail@uwm.edu",
                          "555-5555", "123 Fake Street")

    def test_edit_userUsername(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user, "newUsername")

    def test_edit_userUsernameEmpty(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch empty username"):
            self.ad.edit_user(user, "")

    def test_edit_userPassword(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user, password="newPass")

    def test_edit_userPasswordEmpty(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch empty password"):
            self.ad.edit_user(user, password="")

    def test_edit_userName(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        self.ad.edit_user(user, name="New Name")

    def test_edit_userNameEmpty(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch empty name"):
            self.ad.edit_user(user, name="")

    def test_edit_userNameNonString(self):
        user = self.ad.create_user("newuser", "password", "New", "TA", "email@uwm.edu")
        with self.assertRaises(ValueError, msg="Fails to catch invalid value type"):
            self.ad.edit_user(user, name=123)

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
        pass

    def test_delete_course(self):
        pass

    def test_create_section(self):
        pass

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
