from django.views import View
from django.shortcuts import render, redirect

from ta_app.Classes.CourseClass import CourseClass
from ta_app.models import Course, Semesters


class editCourse(View):
    def get(self, request, course_pk):
        semesters = Semesters.choices  # get the semester choice options
        course = Course.objects.get(pk=course_pk)  # get the current course

        current = request.session["role"]
        if current == "Admin":
            return render(request, "edit_course.html", {'semesters': semesters, 'course': course})
        else:
            return redirect('/Home/')

    def post(self, request, course_pk):
        semesters = Semesters.choices  # get the semester choice options
        course = Course.objects.get(pk=course_pk)  # get the current course

        # Extract form data - set no input to None
        courseNumber = request.POST.get("course_id", None)
        courseid = ""
        if courseNumber is not None:
            courseid = int(courseNumber)
        course_name = request.POST.get("course_name", None)
        description = request.POST.get("description", None)
        semester = request.POST.get("semester", None)

        # Create a CourseClass object with the new data
        new_course = CourseClass(course_id=course.course_id, course_name=course.course_name,
                                 description=course.description, semester=course.semester)

        # Call the edit_course method of the CourseClass object
        try:
            new_course.edit_course(course_id=courseid, course_name=course_name, description=description,
                                   semester=semester)
            course = Course.objects.get(pk=course_pk)
            return render(request, "edit_course.html",
                          {'semesters': semesters, 'course': course, 'errorMessage': "Course edited successfully!"})
        except ValueError as e:
            return render(request, "edit_course.html",
                          {'semesters': semesters, 'course': course, 'errorMessage': str(e)})
