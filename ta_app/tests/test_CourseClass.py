from django.test import TestCase
from ta_app.Classes.CourseClass import CourseClass


class CommonCourses(TestCase):
    def setUp(self):
        self.default = CourseClass(0, "test name", "test description", "Fall")
        self.cs361 = CourseClass(361, "CompSci", "A computer science course", "Spring")
        self.duplicateDefault = CourseClass(0, "test name", "test description", "Fall")


class CourseInit(CommonCourses):
    def test_courseFourArg(self):
        # will the Four-argument constructor produce the correct id, name, description, and semester?
        temp = self.default
        self.assertEqual(0, temp.course_id, "course_id is incorrect value")
        self.assertEqual("test name", temp.course_name, "course_name is incorrect value")
        self.assertEqual("test description", temp.description, "course description is incorrect value")
        self.assertEqual("Fall", temp.semester, "course semester is incorrect value")

    def test_idInputString(self):
        # will constructor throw an exception if string data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Non-numeric ID data fails to raise TypeError"):
            CourseClass("X", "test name", "test description", "Fall")

    def test_idInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_id?
        with self.assertRaises(TypeError, msg="Float ID data fails to raise TypeError"):
            CourseClass(1.1, "test name", "test description", "Fall")

    def test_idInputNegative(self):
        # will constructor throw an exception if negative data is passed to the course_id?
        # Rule: negative IDs will not be allowed
        with self.assertRaises(ValueError, msg="Negative ID data fails to raise ValueError"):
            CourseClass(-1, "test name", "test description", "Fall")

    def test_nameInputInt(self):
        # will constructor throw an exception if int data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Integer name data fails to raise TypeError"):
            CourseClass(0, 1, "test description", "Fall")

    def test_nameInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the course_name?
        with self.assertRaises(TypeError, msg="Float name data fails to raise TypeError"):
            CourseClass(0, 1.1, "test description", "Fall")

    def test_nameInputWhiteSpaceGood(self):
        # will any leading and trailing whitespace surrounding the course_name be removed and allow a
        # CourseClass object to be created
        temp = CourseClass(0, "  test name  ", "test description", "Fall")
        self.assertEqual("test name", temp.course_name, "course name is incorrect value")

    def test_nameInputWhiteSpaceOnly(self):
        # will constructor throw an exception if course_name only contains whitespace
        with self.assertRaises(ValueError, msg="Empty name data fails to raise ValueError"):
            CourseClass(0, "   ", "test description", "Fall")

    def test_nameInputDigit(self):
        # will constructor throw an exception if course_name input is only digits?
        with self.assertRaises(ValueError, msg="Course name as numeric value fails to raise ValueError"):
            CourseClass(0, "123", "test description", "Fall")

    def test_descriptionInputInt(self):
        # will constructor throw an exception if int data is passed to the description?
        with self.assertRaises(TypeError, msg="Integer description data fails to raise TypeError"):
            CourseClass(0, "test name", 1, "Fall")

    def test_descriptionInputFloat(self):
        # will constructor throw an exception if floating-point data is passed to the description?
        with self.assertRaises(TypeError, msg="Float description data fails to raise TypeError"):
            CourseClass(0, "test name", 1.1, "Fall")

    def test_descriptionInputWhiteSpaceGood(self):
        # will any leading and trailing whitespace surrounding the description be removed and allow a
        # CourseClass object to be created
        temp = CourseClass(0, "test name", "  test description  ", "Fall")
        self.assertEqual("test description", temp.description, "course description is incorrect value")

    def test_descriptionInputWhiteSpaceOnly(self):
        # will constructor throw an exception if description only contains whitespace
        with self.assertRaises(ValueError, msg="Empty description data fails to raise ValueError"):
            CourseClass(0, "test name", "   ", "Fall")

    def test_descriptionInputTrimIsDigit(self):
        # will constructor allow a CourseClass object be created that has a description that is a
        # string of just digits?
        temp = CourseClass(0, "test name", " 123 ", "Fall")
        self.assertEqual("123", temp.description, "course description is incorrect value")

    def test_semesterNonString(self):
        # will the constructor allow a CourseClass object to be created with an int value as semester?
        with self.assertRaises(ValueError, msg="Incorrect semester input fails to raise ValueError"):
            CourseClass(0, "test name", "test description", 1)

    def test_semesterInputNone(self):
        # will the constructor allow a CourseClass object to be created with no semester input?
        with self.assertRaises(ValueError, msg="Incorrect semester input fails to raise ValueError"):
            CourseClass(0, "test name", "test description", None)

    def test_semesterBad(self):
        # will the constructor allow a CourseClass object to be created with a string value that is not one of
        # the accepted 4 accepted choices?
        with self.assertRaises(ValueError, msg="Incorrect semester input fails to raise ValueError"):
            CourseClass(0, "test name", "test description", "Bad")

    def test_semesterSPRI(self):
        # will the constructor allow a CourseClass object to be created with the wrong semester value representation?
        with self.assertRaises(ValueError, msg="Incorrect semester input fails to raise ValueError"):
            CourseClass(0, "test name", "test description", "SPRI")


class CourseString(CommonCourses):
    def test_displayCourse(self):
        # will string method produce the correct output
        # Rule: string representation will be "<course_name>-<course_id> - <semester>"
        self.assertEqual("test name-0 - Fall", str(self.default), "incorrect string representation returned")


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

    def test_setNameStringDigit(self):
        # will set_name prevent a string of only digits from being set as course_name?
        with self.assertRaises(ValueError, msg="Course name as numeric value fails to raise ValueError"):
            self.default.set_name("123")

    def test_setNameWhiteSpaceOnly(self):
        # will set_name prevent input of only whitespace from being set as the course_name?
        with self.assertRaises(ValueError, msg="Empty course name data fails to raise ValueError"):
            self.default.set_name("   ")

    def test_setNameWhiteSpaceGood(self):
        # will set_name properly trim any leading or trailing whitespace from the input?
        self.default.set_name("  CompSci  ")
        self.assertEqual("CompSci", self.default.course_name, "Course name is incorrect value")


class CourseSetDescription(CommonCourses):
    def test_setDescriptionNoInput(self):
        # will no input cause set_description to throw an exception
        with self.assertRaises(TypeError, msg="No input fails to raise TyperError"):
            self.default.set_description(None)

    def test_setDescriptionNonString(self):
        # will passing non-string data cause set_name to throw an exception?
        with self.assertRaises(TypeError, msg="Non-string description data fails to raise TypeError"):
            self.default.set_description(1)

    def test_setDescriptionString(self):
        # will set_description properly change the course's description field?
        self.default.set_description("test test test")
        self.assertEqual("test test test", self.default.description,
                         "Course description is not updated by set_description")

    def test_setDescriptionWhiteSpaceOnly(self):
        # will set_description prevent input of only whitespace from being set as the description?
        with self.assertRaises(ValueError, msg="Empty description data fails to raise ValueError"):
            self.default.set_description("   ")

    def test_setDescriptionWhiteSpaceGood(self):
        # will set_description properly trim any leading or trailing whitespace from the input?
        self.default.set_description("  A computer science course  ")
        self.assertEqual("A computer science course", self.default.description, "Course description is incorrect value")

    def test_setDescriptionIsDigit(self):
        # will set_description allow input of only digits to be set as the description of a CourseClass object?
        self.default.set_description("  123  ")
        self.assertEqual("123", self.default.description, "Course description is incorrect value")


class ClassCourseSetSemester(CommonCourses):
    def test_setSemesterNoInput(self):
        # will set_semester allow no input to be set as the semester of a CourseClass object?
        with self.assertRaises(ValueError, msg="No input fails to raise ValueError"):
            self.default.set_semester(None)

    def test_setSemesterNonString(self):
        # will set_semester allow non-string data to be set as the semester of a CourseClass object?
        with self.assertRaises(ValueError, msg="Int input for course semester fails to raise ValueError"):
            self.default.set_semester(1)

    def test_setSemesterBad(self):
        # will set_semester allow string data that is not one of four acceptable choices to be set as the
        # semester of a CourseClass object?
        with self.assertRaises(ValueError, msg="Input that is not one of acceptable choices fails to raise ValueError"):
            self.default.set_semester("Bad")

    def test_setSemesterAllCaps(self):
        # will set_semester allow string data with incorrect capitalization to be set as the semester of a
        # CourseClass object?
        # Note: we plan to control the choice options available to the user, so this helps ensure that the data coming
        # in is what we want and, thus, consistently comparable.
        with self.assertRaises(ValueError, msg="Input that is not one of acceptable choices fails to raise ValueError"):
            self.default.set_semester("FALL")

    def test_setSemesterEmptyString(self):
        # will set_semester allow string data that is not one of four acceptable choices to be set as the
        # semester of a CourseClass object?
        with self.assertRaises(ValueError, msg="Input that is not one of acceptable choices fails to raise ValueError"):
            self.default.set_semester("")

    # ensure that we are capable of setting each of the four possibilities
    def test_setSemesterFall(self):
        # will set_semester successfully set the semester of a CourseClass object for Fall?
        self.cs361.set_semester("Fall")
        self.assertEqual("Fall", self.cs361.semester, "Fall semester was not set properly")

    def test_setSemesterSpring(self):
        # will set_semester successfully set the semester of a CourseClass object for Spring?
        self.default.set_semester("Spring")
        self.assertEqual("Spring", self.default.semester, "Spring semester was not set properly")

    def test_setSemesterWinter(self):
        # will set_semester successfully set the semester of a CourseClass object for Winter?
        self.default.set_semester("Winter")
        self.assertEqual("Winter", self.default.semester, "Winter semester was not set properly")

    def test_setSemesterSummer(self):
        # will set_semester successfully set the semester of a CourseClass object for Summer?
        self.default.set_semester("Summer")
        self.assertEqual("Summer", self.default.semester, "Summer semester was not set properly")


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


class CourseGetCourseSemester(CommonCourses):
    def test_getSemester(self):
        # will get_semester return the course's current description?
        self.assertEqual("Fall", self.default.get_course_semester(),
                         "Value returned by get_course_semester is incorrect")


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
        temp2 = CourseClass(0, "test name", "new description", "Fall")
        temp1.create_course()
        self.assertEqual(False, temp2.create_course(),
                         "Adding a duplicate course with different description did not return False")

    def test_addSameNameAndSemesterDifferentID(self):
        # will create_course allow two courses with the same name and semester but different IDs to be added?
        temp1 = self.cs361
        temp2 = CourseClass(351, "CompSci", "A computer science course", "Spring")
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(),
                         "Adding a course with same name and semester but different ID did not return True")

    def test_addSameNameDifferentIDAndSemester(self):
        # will create_course allow two courses with the same name but different IDs and semesters to be added?
        temp1 = self.cs361
        temp2 = CourseClass(351, "CompSci", "A computer science course", "Fall")
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(),
                         "Adding a course with same name but different ID and semester did not return True")

    def test_addSameIDAndSemesterDifferentName(self):
        # will create_course allow two courses with the same ID and semester but different name be added?
        temp1 = self.cs361
        temp2 = CourseClass(361, "Anthro", "An anthropology course", "Spring")
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(),
                         "Adding a course with same ID and semester but different name did not return True")

    def test_addSameIDDifferentNameAndSemester(self):
        # will create_course allow two courses with the same ID and semester but different name and semester be added?
        temp1 = self.cs361
        temp2 = CourseClass(361, "Anthro", "An anthropology course", "Fall")
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(),
                         "Adding a course with same ID but different name and semester did not return True")

    def test_addSameIDandNameDifferentSemester(self):
        # will create_course allow two courses with the same ID and name but different semester be added?
        temp1 = self.cs361
        temp2 = CourseClass(361, "CompSci", "A computer science course", "Fall")
        temp1.create_course()
        self.assertEqual(True, temp2.create_course(),
                         "Adding a course with same ID and name but different semester did not return True")

    def test_addSameWhiteSpace(self):
        # will CourseClass constructor return duplicate courses correctly to prevent duplicate database additions
        temp1 = self.cs361
        temp2 = CourseClass(361, " CompSci ", " A computer science course ", "Fall")
        temp1.create_course()
        self.assertEqual(False, temp2.create_course(), "Course objects should have been duplicates")
