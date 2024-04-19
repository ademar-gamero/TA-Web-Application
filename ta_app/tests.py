from django.test import TestCase
from ta_app.Classes.Course import Course


# Create your tests here.
class CommonCourses(TestCase):
    def setUp(self):
        self.default = Course(0, "test name", "test description")


class CourseInit(CommonCourses):
    def test_courseThreeArg(self):
        # will the three-argument constructor produce the correct id, name, and description?
        temp = self.default
        self.assertEqual(0, temp.course_id, "course_id is incorrect value")
        self.assertEqual("test name", temp.course_name, "course_name is incorrect value")
        self.assertEqual("test description", temp.description, "course description is incorrect value")

    def test_defaultCourse(self):
        # will the 0 argument version of the constructor produce the correct id, name, and description?
        temp = Course()
        self.assertEqual(0, temp.course_id, "Default ID is incorrect value")
        self.assertEqual("unavailable", temp.course_name, "Default name is incorrect value")
        self.assertEqual("TBD", temp.description, "Default description is incorrect value")

    def test_idInputString(self):
        # will constructor throw an exception if string data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Non-numeric ID data fails to raise TypeError"):
            Course("X", "test name", "test description")

    def test_idInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Float ID data fails to raise TypeError"):
            Course(1.1, "test name", "test description")

    def test_idInputNegative(self):
        # will constructor throw an exception if negative data is passed to the course_id?
        # Rule: negative IDs will not be allowed
        with self.assertRaises(ValueError, msg="Negative ID data fails to raise ValueError"):
            Course(-1, "test name", "test description")

    def test_nameInputInt(self):
        # will constructor throw an exception if int data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Integer name data fails to raise TypeError"):
            Course(0, 1, "test description")

    def test_nameInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Float name data fails to raise TypeError"):
            Course(0, 1.1, "test description")

    def test_descriptionInputInt(self):
        # will constructor throw an exception if int data is passed to the description?
        with self.assertRaises(TypeError, msg="Integer description data fails to raise TypeError"):
            Course(0, "test name", 1)

    def test_descriptionInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the description?
        with self.assertRaises(TypeError, msg="Float description data fails to raise TypeError"):
            Course(0, "test name", 1.1)


class CourseString(CommonCourses):
    def test_displayCourse(self):
        # will string method produce the correct output
        # Rule: string representation will be "<course_name> - <course_id>"
        self.assertEqual("test name - 0", str(self.default), "incorrect string representation returned")


class CourseSetID(CommonCourses):
    def test_setIdNoInput(self):
        # will no input cause set_id to throw an exception?
        with self.assertRaises(TypeError, msg="No input fails to raise TypeError"):
            self.default.set_id(None)

    def test_setIdNegative(self):
        # will passing negative data to set_id throw an exception
        # Rule: set_id will not accept negative values. (ID must be >= 0)
        with self.assertRaises(ValueError, msg="Negative ID data fails to raise ValueError"):
            self.default.set_id(-1)

    def test_setIdFloat(self):
        # will floating-point data passed to set_id throw an exception?
        with self.assertRaises(TypeError, msg="Float ID data fails to raise TypeError"):
            self.default.set_id(3.61)

    def test_setIdString(self):
        # will string data passed to set_id throw an exception?
        with self.assertRaises(TypeError, msg="String ID data fails to raise TypeError"):
            self.default.set_id("test")

    def test_setIdInt(self):
        # will set_id properly change the course's id field?
        self.default.set_id(361)
        self.assertEqual(361, self.default.course_id, "Course ID is not updated by set_id")


class CourseSetName(CommonCourses):
    def test_setNameNoInput(self):
        # will no parameter set_name throw an exception?
        with self.assertRaises(TypeError, msg="No input fails to raise TyperError"):
            self.default.set_name(None)

    def test_setNameNonString(self):
        # will passing non-string data cause set_name to throw an exception?
        with self.assertRaises(TypeError, msg="Non-string name data fails to raise TypeError"):
            self.default.set_name(1)

    def test_setNameString(self):
        # will set_name properly change the course's name field?
        self.default.set_name("CompSci")
        self.assertEqual("CompSci", self.default.course_name, "Course name is not updated by set_name")


class CourseSetDescription(CommonCourses):
    def test_setDescriptionNoInput(self):
        # will no input cause set_description to throw an exception
        with self.assertRaises(TypeError, msg="No input fails to raise TyperError"):
            self.default.description(None)

    def test_setDescriptionNonString(self):
        # will passing non-string data cause set_name to throw an exception?
        with self.assertRaises(TypeError, msg="Non-string description data fails to raise TypeError"):
            self.default.description(1)

    def test_setDescriptionString(self):
        # will set_description properly change the course's description field?
        self.default.set_description("test test test")
        self.assertEqual("test test test", self.default.description,
                         "Course description is not updated by set_description")


class CourseGetCourseID(CommonCourses):
    def test_getID(self):
        # will get_course_id return the course's current id?
        self.assertEqual(0, self.default.get_course_id(), "Value returned by get_course_id is incorrect")


class CourseGetCourseName(CommonCourses):
    def test_getName(self):
        # will get_course_name return the course's current name?
        self.assertEqual("test name", self.default.get_course_name(),
                         "Value returned by get_course_name is incorrect")


class CourseGetCourseDescription(CommonCourses):
    def test_getDescription(self):
        # will get_course_description return the course's current description?
        self.assertEqual("test description", self.default.get_course_description(),
                         "Value returned by get_course_description is incorrect")
