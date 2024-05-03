from django.shortcuts import render, redirect
from django.views import View
from ta_app.models import Course
from django.contrib import messages

class courseList(View):
    def get(self, request):
        if 'role' not in request.session or 'name' not in request.session:
            messages.error(request, "You are not logged in.")
            return redirect('login')
        courses = Course.objects.all()
        is_admin = request.session.get('role') == 'Admin'  # Check if user is an admin
        return render(request, "courseList.html", {"courselist": courses, "is_admin": is_admin})

    def post(self, request):
        # Handle deletion confirmation for admins
        if 'delete_id' in request.POST and request.session.get('role') == 'Admin':
            course_id = request.POST.get('delete_id')
            try:
                course = Course.objects.get(id=course_id)
                course.delete()
                messages.success(request, 'Course successfully deleted.')
            except Course.DoesNotExist:
                messages.error(request, 'Course not found.')
        return redirect('courseList')
