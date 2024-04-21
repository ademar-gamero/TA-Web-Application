class Course(object):
    def __init__(self, course_id=0, course_name="unavailable", description="TBD"):
        self.set_id(course_id)
        self.set_name(course_name)
        self.set_description(description)

    def __str__(self):
        return f"{self.course_name} - {self.course_id}"

    def set_name(self, course_name):
        if not isinstance(course_name, str):
            raise TypeError("ID must be an integer")
        self.course_name = course_name

    def set_id(self, course_id):
        if not isinstance(course_id, int):
            raise TypeError("ID must be an integer")
        elif course_id < 0:
            raise ValueError("ID cannot be negative")
        self.course_id = course_id

    def set_description(self, description):
        if not isinstance(description, str):
            raise TypeError("ID must be an integer")
        self.description = description

    def get_course_id(self):
        return self.course_id

    def get_course_name(self):
        return self.course_name

    def get_course_description(self):
        return self.description
