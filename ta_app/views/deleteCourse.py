from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import Course
from django.contrib import messages

class deleteCourse(View):
    def get(self, request, course_id):
        role = request.session['role'];
        if role != "Admin":
            return redirect('courseList')
        if 'role' not in request.session or request.session['role'] != 'Admin':
            messages.error(request, "You are not authorized to view this page.")
            return redirect('courseList')

        course = Course.objects.filter(pk=course_id).first()
        if course:
            return render(request, 'delete_course.html', {'course': course})
        else:
            messages.error(request, 'Course not found!')
            return redirect('courseList')

    def post(self, request, course_id):
        if 'role' in request.session and request.session['role'] == 'Admin':
            if 'confirm' in request.POST:
                course = Course.objects.filter(pk=course_id).first()
                if course:
                    course.delete()
                    messages.success(request, 'Course deleted successfully!')
                else:
                    messages.error(request, 'Course not found!')
            return redirect('courseList')
        else:
            messages.error(request, "Unauthorized attempt to delete a course.")
            return redirect('courseList')