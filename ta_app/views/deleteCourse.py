from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import Course
from django.contrib import messages

class deleteCourse(View):
    def get(self, request, course_id):
        if 'role' not in request.session or 'name' not in request.session:
            messages.error(request, "You are not logged in.")
            return redirect('login')
        course = Course.objects.filter(pk=course_id).first()
        if course:
            return render(request, 'delete_course.html', {'course': course})
        else:
            messages.error(request, 'Course not found!')
            return redirect('courseList')

    def post(self, request, course_id):
        # Perform the actual deletion if confirmed
        if 'confirm' in request.POST:
            course = Course.objects.filter(pk=course_id).first()
            if course:
                course.delete()
                messages.success(request, 'Course deleted successfully!')
            else:
                messages.error(request, 'Course not found!')
        return redirect('courseList')