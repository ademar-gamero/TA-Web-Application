from django.shortcuts import render, redirect
from django.views import View
from ta_app.Classes.CourseClass import CourseClass
from ta_app.models import Semesters


# Create your views here.
class createCourse(View):
    def get(self, request):
        semesters = Semesters.choices  # get the semester choice options

        # make sure that the user is of appropriate role status
        current = request.session["role"]
        if current == "Admin":
            return render(request, "create_course.html", {'semesters': semesters})
        else:
            return redirect('/Home/')

    def post(self, request):
        semester = request.POST.get("semester")
        courseNumber = request.POST.get("course_id")
        courseid=""
        if courseNumber != '':
            courseid = int(courseNumber)
        name = request.POST.get("course_name")
        description = request.POST.get("description")

        semesters = Semesters.choices  # get the semester choice options

        course = None  # tracks if the CourseClass object has been successfully created (data validation)
        check = False  # tracks if the course has been successfully added to the database
        try:
            course = CourseClass(course_id=courseid, course_name=name, description=description, semester=semester)
        except TypeError as e:
            return render(request, "create_course.html", {'semesters': semesters, 'errorMessage': e.__str__()})
        except ValueError as e:
            return render(request, "create_course.html", {'semesters': semesters, 'errorMessage': e.__str__()})

        check = course.create_course()  # set flag to value returned by the method responsible for database additions

        if check == True:
            return render(request, "create_course.html", {'semesters': semesters,
                                                          'errorMessage': "Course Created Successfully!"})
        else:
            return render(request, "create_course.html", {'semesters': semesters,
                                                          'errorMessage': "Duplicate course not added!"})
