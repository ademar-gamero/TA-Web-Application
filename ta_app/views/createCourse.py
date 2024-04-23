from django.shortcuts import render
from django.views import View
from ta_app.Classes.CourseClass import CourseClass


# Create your views here.
class createCourse(View):
    def get(self, request):
        return render(request, "create_course.html", {})

    def post(self, request):
        courseNumber = request.POST.get("course_id")
        courseid = int(courseNumber)
        name = request.POST.get("course_name")
        description = request.POST.get("description")
        # We want these to return None if there's nothing there, so don't add the second parameter. The
        # default in this case will automatically be None.
        # So the CourseClass() constructor will throw a TypeError if we try to create an instance of
        # the class with one of the parameters as None. Our try except block, here in the post method,
        # will then throw an exception and nothing will actually be posted to the database.

        check = False
        course = None
        try:
            course = CourseClass(course_id=courseid, course_name=name, description=description)
        except TypeError as e:
            return render(request, "create_course.html", {'check': check, 'errorMessage': e.__str__()})
        except ValueError as e:
            return render(request, "create_course.html", {'check': check, 'errorMessage': e.__str__()})

        if course.create_course() == True:  # if "course.create_course() returns True"
            check = True

        return render(request, "create_course.html", {'check': check})
