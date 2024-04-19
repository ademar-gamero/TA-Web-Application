class Course(object):
    def __init__(self, course_id=0, course_name="unavailable", description="TBD"):
        self.course_id = course_id
        self.course_name = course_name
        self.description = description

    def __str__(self):
        pass

    def set_name(self, course_name):
        pass

    def set_id(self, course_id):
        pass

    def set_description(self, description):
        pass

    def get_course_id(self):
        pass

    def get_course_name(self):
        pass

    def get_course_description(self):
        pass
