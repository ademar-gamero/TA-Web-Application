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
            try:
                course = Course.objects.get(pk=course_pk)
            except Course.DoesNotExist:
                messages.error(request, "Course not found. Returning to course list.")
                return redirect('courseList')
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                messages.error(request, "User not found. Returning to course sections page.")
                return redirect('courseSections')
            return render(request, "remove_courseAssignment.html", context={"user": user, "course": course})
        else:
            messages.error(request, "You are not authorized to view this page.")
            return redirect('/Home/')

    def post(self, request, user_pk, course_pk):
        pass