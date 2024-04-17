from django.test import TestCase
from ta_app.Classes.course import Course


# Create your tests here.
class CommonCourses(TestCase):
    def setUp(self):
        self.default = Course(0, "test name", "test description")


class CourseInit(TestCase):
    def test_courseThreeArgId(self):
        self.assertEqual(0, Course(0, "test name", "test description").course_id,
                         "course_id is incorrect value")

    def test_courseThreeArgName(self):
        self.assertEqual("test name", Course(0, "test name", "test description").course_name,
                         "course_name is incorrect value")

    def test_courseThreeArgDescription(self):
        self.assertEqual("test description", Course(0, "test name", "test description").description,
                         "course description is incorrect value")

    def test_defaultId(self):  # check if we want to allow default values
        # will the 0 argument version of the constructor produce the correct id?
        self.assertEqual(0, Course().course_id, "Default ID is incorrect value")

    def test_defaultName(self):
        # will the 0 argument version of the constructor produce the correct name?
        self.assertEqual("unavailable", Course().course_name, "Default name is incorrect value")

    def test_defaultDescription(self):
        # will the 0 argument version of the constructor produce the correct description?
        self.assertEqual("TBD", Course().description, "Default description is incorrect value")

    def test_idInputString(self):
        # will constructor throw an exception if string data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Non-numeric ID data fails to raise TypeError") as ctx:
            a = Course("X", "test name", "test description")
        self.assertEqual(str(ctx.exception), "Non-numeric ID data fails to raise TypeError")

    def test_idInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Float ID data fails to raise TypeError") as ctx:
            a = Course(1.1, "test name", "test description")
        self.assertEqual(str(ctx.exception), "Float ID data fails to raise TypeError")

    def test_idInputNegative(self):
        # will constructor throw an exception if negative data is passed to the course_id?
        # Rule: negative IDs will not be allowed
        with self.assertRaises(ValueError, msg="Negative ID data fails to raise ValueError") as ctx:
            a = Course(-1, "test name", "test description")
        self.assertEqual(str(ctx.exception), "Negative ID data fails to raise ValueError")

    def test_nameInputInt(self):
        # will constructor throw an exception if int data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Integer name data fails to raise TypeError") as ctx:
            a = Course(0, 1, "test description")
        self.assertEqual(str(ctx.exception), "Integer name data fails to raise TypeError")

    def test_nameInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Float name data fails to raise TypeError") as ctx:
            a = Course(0, 1.1, "test description")
        self.assertEqual(str(ctx.exception), "Float name data fails to raise TypeError")

    def test_descriptionInputInt(self):
        # will constructor throw an exception if int data is passed to the description?
        with self.assertRaises(TypeError, msg="Integer description data fails to raise TypeError") as ctx:
            a = Course(0, "test name", 1)
        self.assertEqual(str(ctx.exception), "Integer description data fails to raise TypeError")

    def test_descriptionInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the description?
        with self.assertRaises(TypeError, msg="Float description data fails to raise TypeError") as ctx:
            a = Course(0, "test name", 1.1)
        self.assertEqual(str(ctx.exception), "Float description data fails to raise TypeError")


class CourseString(CommonCourses):
    def test_displayCourse(self):
        # will string method produce the correct output
        # Rule: string representation will be "<course_name>"
        self.assertEqual("test name", str(self.default), "incorrect string representation returned")
