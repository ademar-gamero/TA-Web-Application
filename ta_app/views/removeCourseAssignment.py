from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import Course, User, Section
from django.contrib import messages
from ta_app.Classes.UserClass import UserClass


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
        try:
            course = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            messages.error(request, "Course not found. Returning to course list.")
            return redirect('courseList')
        try:
            user = User.objects.get(pk=user_pk)
            u = UserClass(username=user.username, password=user.password, name=user.name, role=user.role,
                          email=user.email, phone_number=user.phone_number, address=user.address,assigned=user.assigned,
                          assigned_sections=user.assigned_section.all())
            sections = user.assigned_section.filter(course_parent=course_pk, type="LEC").all()
            removed = False
            for section in sections:
                try:
                    u.remove_section(section)
                    removed = True
                except ValueError as e:
                    messages.error(request, e.__str__())
            if removed:
                messages.success(request, user.__str__() + ' successfully removed from ' + course.__str__())
        except User.DoesNotExist:
            messages.error(request, "User not found. Returning to course sections page.")
        return redirect('courseSections', course_pk=course_pk)