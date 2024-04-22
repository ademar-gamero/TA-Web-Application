class CourseClass(object):
    def __init__(self, course_id, course_name, description):
        # want to redo this method a little bit different
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        pass

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
        # New method. Will add the calling CourseClass object to the database,
        # but will not allow ID+name combo duplicates.
        pass
