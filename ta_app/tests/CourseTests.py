from django.test import TestCase
from ta_app.classes.CourseClass import CourseClass


# Create your tests here.
class CommonCourses(TestCase):
    def setUp(self):
        self.default = CourseClass(0, "test name", "test description")
        self.cs361 = CourseClass(361, "CompSci", "A computer science course")
        self.duplicateDefault = CourseClass(0, "test name", "test description")


class CourseInit(CommonCourses):
    def test_courseThreeArg(self):
        # will the three-argument constructor produce the correct id, name, and description?
        temp = self.default
        self.assertEqual(0, temp.course_id, "course_id is incorrect value")
        self.assertEqual("test name", temp.course_name, "course_name is incorrect value")
        self.assertEqual("test description", temp.description, "course description is incorrect value")

    def test_idInputString(self):
        # will constructor throw an exception if string data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Non-numeric ID data fails to raise TypeError"):
            CourseClass("X", "test name", "test description")

    def test_idInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Float ID data fails to raise TypeError"):
            CourseClass(1.1, "test name", "test description")

    def test_idInputNegative(self):
        # will constructor throw an exception if negative data is passed to the course_id?
        # Rule: negative IDs will not be allowed
        with self.assertRaises(ValueError, msg="Negative ID data fails to raise ValueError"):
            CourseClass(-1, "test name", "test description")

    def test_nameInputInt(self):
        # will constructor throw an exception if int data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Integer name data fails to raise TypeError"):
            CourseClass(0, 1, "test description")

    def test_nameInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Float name data fails to raise TypeError"):
            CourseClass(0, 1.1, "test description")

    def test_descriptionInputInt(self):
        # will constructor throw an exception if int data is passed to the description?
        with self.assertRaises(TypeError, msg="Integer description data fails to raise TypeError"):
            CourseClass(0, "test name", 1)

    def test_descriptionInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the description?
        with self.assertRaises(TypeError, msg="Float description data fails to raise TypeError"):
            CourseClass(0, "test name", 1.1)


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


class CourseCreateCourse(CommonCourses):
    def test_addSingle(self):
        # will the create_course method return the correct value when a single course is added?
        temp = self.default
        self.assertEqual(True, temp.create_course(), "Adding course did not return True")

    def test_addMultiple(self):
        # will the create_course method allow adding two courses with all different fields?
        temp1 = self.default
        temp2 = self.cs361
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(), "Adding second course did not return True")

    def test_addSameTwice(self):
        # will the create_course method return False when trying to add the same course twice?
        temp = self.default
        temp.create_course()
        self.assertEqual(False, temp.create_course(), "Adding the same course twice did not return False")

    def test_addDuplicate(self):
        # will the create_course method return False when trying to add a course with all duplicate fields?
        temp1 = self.default
        temp2 = self.duplicateDefault
        temp1.create_course()
        self.assertEqual(False, temp2.create_course(), "Adding a duplicate course did not return False")

    def test_addDuplicateDifferentDescription(self):
        # will trying to call create_course with a course with same ID and same name,
        # but different description be allowed?
        temp1 = self.default
        temp2 = CourseClass(0, "test name", "new description")
        temp1.create_course()
        self.assertEqual(False, temp2.create_course(),
                         "Adding a duplicate course with different description did not return False")

    def test_addSameNameDifferentID(self):
        # will create_course allow two courses with the same name but different IDs to be added?
        temp1 = self.cs361
        temp2 = CourseClass(351, "CompSci", "A computer science course")
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(),
                         "Adding a course with same name but different ID did not return True")

    def test_addSameIDDifferentName(self):
        # will create_course allow two courses with the same ID but different name be added?
        temp1 = self.cs361
        temp2 = CourseClass(361, "Anthro", "An anthropology course")
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(),
                         "Adding a course with same ID but different name did not return True")
