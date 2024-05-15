from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import Course, User, Section
from django.contrib import messages


class removeCourseAssignment(View):
    def get(self, request, user_pk, course_pk):
        if 'role' not in request.session or 'name' not in request.session:
            messages.error(request, "You are not logged in.")
            return redirect('login')
        current = request.session["role"]
        if current == "Admin":
            user = None
            course = None
            message = ""
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                successful = False
                message = "Error: User not found."
                if user is not None:
                    try:
                        course = Course.objects.get(pk=course_pk)
                    except Course.DoesNotExist:
                        message = "Error: Course not found"
            return render(request, "remove_courseAssignment.html", context={"user": user, "course": course, "message": message})
        else:
            return redirect('/Home/')

    def post(self, request, user_pk, course_pk):
        pass