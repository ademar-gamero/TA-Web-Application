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
        old_id = self.get_course_id()
        old_name = self.get_course_name()
        old_description = self.get_course_description()
        old_semester = self.get_course_semester()

        # Get the calling course that we want to edit (there should only be one option ever returned... or none)
        # Protect against trying to edit a course that does not exist in the database.
        try:
            course = Course.objects.get(course_id=old_id, course_name=old_name, semester=old_semester)
        except Course.DoesNotExist:
            raise ValueError("Course not found!")

        # Use setters to edit each field that the user has provided input to edit. The setters will raise an error
        # if any of the input values do not pass the validation.
        try:
            check = False
            if course_id is not None:
                check = True
                self.set_id(course_id)
            if course_name is not None:
                check = True
                self.set_name(course_name)
            if description is not None:
                self.set_description(description)
            if semester is not None:
                check = True
                self.set_semester(semester)
            if check:  # if we have changed any one of the three critical values (ID, name, and/or semester)
                # check the database to see if the course we are attempting to make already exists and raise
                # an error if so
                try:
                    Course.objects.get(course_id=self.course_id, course_name=self.course_name, semester=self.semester)
                    # edge case (when only description is being changed)
                    count = Course.objects.filter(course_id=self.course_id, course_name=self.course_name, semester=self.semester, description=self.description).count()
                    if count == 0 and self.description != old_description:
                        Course.objects.filter(pk=course.pk).update(description=self.description)
                        return True
                    else:
                        # It is creating a conflicting course, so reset all values back to original
                        self.course_id = old_id
                        self.course_name = old_name
                        self.description = old_description
                        self.semester = old_semester
                        raise ValueError("Exact course already exists!")
                except Course.DoesNotExist:
                    pass  # do nothing. If it doesn't already exist, we're good to go!
            # Now we can update all values in the database.
            Course.objects.filter(pk=course.pk).update(course_id=self.course_id, course_name=self.course_name,
                                                       description=self.description, semester=self.semester)
            return True
        except TypeError or ValueError as e:
            # If any validation fails during setters, reset all values back to original
            self.course_id = old_id
            self.course_name = old_name
            self.description = old_description
            self.semester = old_semester
            raise ValueError(e.__str__())
