from ta_app.models import Course


class CourseClass(object):
    def __init__(self, course_id, course_name, description, semester):
        # course_id data validation:
        if not isinstance(course_id, int):
            raise TypeError("ID must be an integer")
        elif course_id < 0:
            raise ValueError("ID cannot be negative")

        # course_name data validation:
        # check that it is the correct type first
        if not isinstance(course_name, str):
            raise TypeError("Course name must be a string")
        # now we can assume that it is a string and trim all leading and trailing whitespace
        course_name = course_name.strip()
        if not course_name:  # "if course_name is an empty string"
            raise ValueError("Course name cannot be empty")
        if course_name.isdigit():  # check if the value is just a string of numeric digits
            raise ValueError("Course name should not be solely numeric digits")

        # description data validation:
        if not isinstance(description, str):
            raise TypeError("Course description must be a string")
        description = description.strip()
        if not description:
            raise ValueError("Course description cannot be left empty")
        # Note: the user should have more freedom with the description input, thus, we will allow
        # descriptions that are just digits to be set.

        # semester data validation:
        # Note: this will catch instances of non-string input and None.
        # The plan is to have semester be a dropdown menu on the form, so we should not have to
        # really account for bad user input like leading or trailing whitespace.
        if semester not in ["Fall", "Winter", "Spring", "Summer"]:
            raise ValueError("Invalid semester")

        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.semester = semester

    def __str__(self):
        return f"{self.course_name}-{self.course_id} - {self.semester}"

    def set_name(self, course_name):
        if not isinstance(course_name, str):
            raise TypeError("Course name must be a string")
        course_name = course_name.strip()
        if not course_name:
            raise ValueError("Course name cannot be empty")
        if course_name.isdigit():
            raise ValueError("Course name should not be solely numeric digits")
        self.course_name = course_name

    def set_id(self, course_id):
        if not isinstance(course_id, int):
            raise TypeError("ID must be an integer")
        elif course_id < 0:
            raise ValueError("ID cannot be negative")
        self.course_id = course_id

    def set_description(self, description):
        if not isinstance(description, str):
            raise TypeError("Course description must be a string")
        description = description.strip()
        if not description:
            raise ValueError("Course description cannot be left empty")
        self.description = description

    def set_semester(self, semester):
        if semester not in ["Fall", "Winter", "Spring", "Summer"]:
            raise ValueError("Invalid semester")
        self.semester = semester

    def get_course_id(self):
        return self.course_id

    def get_course_name(self):
        return self.course_name

    def get_course_description(self):
        return self.description

    def get_course_semester(self):
        return self.semester

    def create_course(self):
        # Note: data validation is enforced in the constructor and all setters, thus, we can assume
        # any existing CourseClass objects have valid data
        courseid = self.get_course_id()
        name = self.get_course_name()
        descr = self.get_course_description()
        sem = self.get_course_semester()

        # check that the database does not already contain the id+name+semester combination
        find_course = Course.objects.all().filter(course_id=courseid,course_name=name,semester=sem)
        if find_course.exists():  # if there's something in the returned QuerySet
            return False  # then it already exists

        # otherwise, create new entry and return True
        Course.objects.create(course_id=courseid, course_name=name, description=descr, semester=sem)
        return True

    def edit_course(self, course_id=None, course_name=None, description=None, semester=None):
        # Store old versions of critical course information.
        # (Used to locate the correct entry in the database and fill in for any information that the user does
        # not want to edit).
        old_id = self.get_course_id()
        old_name = self.get_course_name()
        old_description = self.get_course_description()  # might as well
        old_semester = self.get_course_semester()

        # Get the calling course that we want to edit (there should only be one option ever returned... or none)
        # Note: protect against trying to edit a course that does not exist in the database.
        # This happens if we have never successfully called create_course on an existing CourseClass object prior
        # to this point.
        try:
            course = Course.objects.get(course_id=old_id, course_name=old_name, semester=old_semester)
        except Course.DoesNotExist:
            raise ValueError("Course not found!")

        # Edge-case - if only the description is to be edited:
        # Do this before the "default" values substitutions because it's far easier to detect and handle now.
        if course_id is None and course_name is None and semester is None and description is not None:
            if description != old_description:
                self.set_description(description)
                return True

        # substitute in the "default" values for if information is not provided by the user
        if course_id is None:
            course_id = old_id
        if course_name is None:
            course_name = old_name
        if description is None:
            description = old_description
        if semester is None:
            semester = old_semester

        # Note: we need data validation before moving forwards in order to properly search for a match in the
        # database, but we do not want to set any information before we determine if the requested changes
        # will result in any conflicts. This, unfortunately, means that using the setters that are already
        # written (at least as is) will not be possible.

        # ID validation:
        # (Note: don't set yet. The actual lines responsible for updating the CourseClass object need to occur
        # after the filtering confirms that we are not creating duplicates)
        if not isinstance(course_id, int):
            raise TypeError("ID must be an integer")
        elif course_id < 0:
            raise ValueError("ID cannot be negative")

        # Name validation:
        if not isinstance(course_name, str):
            raise TypeError("Course name must be a string")
        course_name = course_name.strip()
        if not course_name:
            raise ValueError("Course name cannot be empty")
        if course_name.isdigit():
            raise ValueError("Course name should not be solely numeric digits")

        # Semester validation:
        if semester not in ["Fall", "Winter", "Spring", "Summer"]:
            raise ValueError("Invalid semester")

        # Description validation:
        if not isinstance(description, str):
            raise TypeError("Course description must be a string")
        description = description.strip()
        if not description:
            raise ValueError("Course description cannot be left empty")

        # Search for if the course already exists in the database for the provided information.
        # We need to protect against allowing the creation of duplicate courses through editing.
        # If this filter returns a result, then we know that we can't allow this edit to go through.
        # If the QuerySet returned is empty, then it is ok, and we can go ahead with the update.
        find_course = Course.objects.all().filter(course_id=course_id, course_name=course_name,
                                                  semester=semester)
        if find_course.exists():  # if there's something in the returned QuerySet
            return False  # then it already exists

        # after we confirm that there will be no conflicts, now we can update the calling object's fields
        self.course_id = course_id
        self.course_name = course_name
        self.semester = semester
        self.description = description

        # Update all database fields for the specific entry
        Course.objects.filter(pk=course.pk).update(
            course_id=course_id,
            course_name=course_name,
            description=description,
            semester=semester
        )
        return True
