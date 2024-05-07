from django.views import View
from django.shortcuts import render, redirect
from ta_app.models import Course, User
from django.contrib import messages

class deleteSection(View):
    def get(self, request, section_id):
        if 'role' not in request.session or request.session['role'] != 'Admin':
            messages.error(request, "You are not authorized to view this page.")
            return redirect('courseList')

        course = Course.objects.filter(pk=section_id).first()
        if course:
            return render(request, 'delete_course.html', {'course': course})
        else:
            messages.error(request, 'Section not found!')
            return redirect('courseList')

    def post(self, request, section_id):
        if 'role' in request.session and request.session['role'] == 'Admin':
            if 'confirm' in request.POST:
                course = Course.objects.filter(pk=section_id).first()
                if course:
                    course.delete()
                    messages.success(request, 'Section deleted successfully!')
                else:
                    messages.error(request, 'Section not found!')
            return redirect('courseList')
        else:
            messages.error(request, "Unauthorized attempt to delete a section.")
            return redirect('courseList')