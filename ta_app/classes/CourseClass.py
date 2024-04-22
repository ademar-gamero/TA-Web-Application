from ta_app.models import Course


class CourseClass(object):
    def __init__(self, course_id, course_name, description):
        if not isinstance(course_id, int):
            raise TypeError("ID must be an integer")
        elif course_id < 0:
            raise ValueError("ID cannot be negative")

        if not isinstance(course_name, str):
            raise TypeError("Course name must be a string")

        if not isinstance(description, str):
            raise TypeError("Course description must be a string")

        self.course_id = course_id
        self.course_name = course_name
        self.description = description

    def __str__(self):
        return f"{self.course_name} - {self.course_id}"

    def set_name(self, course_name):
        if not isinstance(course_name, str):
            raise TypeError("Course name must be a string")
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
        self.description = description

    def get_course_id(self):
        return self.course_id

    def get_course_name(self):
        return self.course_name

    def get_course_description(self):
        return self.description

    def create_course(self):
        # the data validation will happen elsewhere so that whenever it is passed here to
        # be entered into the database, it is already checked to be good
        courseid = self.get_course_id()
        name = self.get_course_name()
        descr = self.get_course_description()

        # check that the database does not already contain the id+name combination
        # return False if it's already there
        find_course = Course.objects.all().filter(course_id=courseid).filter(course_name=name)
        if find_course.exists():  # if there's something in the returned QuerySet
            return False  # then it already exists

        # otherwise, create new entry and return True
        Course.objects.create(course_id=courseid, course_name=name, description=descr)
        return True
