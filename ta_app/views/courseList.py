from django.shortcuts import render, redirect
from django.views import View
from ta_app.models import Course, User, Section
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
        is_admin = request.session.get('role') == 'Admin'  # Check if user is an admin
        user = User.objects.get(pk=request.session['pk'])
        id = request.POST.get('course_id','')
        name = request.POST.get('course_name','')
        semester = request.POST.get('semesters','')
        courses = []
        if request.POST.get('input_btn') == "Submit":
            if id != '' and name == '' and semester == '':
                courses = Course.objects.filter(course_id = int(id))
            if id == '' and name != '' and semester == '':
                courses = Course.objects.filter(course_name = name)
            if id == '' and name == '' and semester != '':
                courses = Course.objects.filter(semester = semester)
            if id != '' and name != '' and semester == '':
                courses = Course.objects.filter(course_id = int(id),course_name = name)
            if id != '' and name == '' and semester != '':
                courses = Course.objects.filter(course_id= int(id),semester = semester)
            if id == '' and name != '' and semester != '':
                courses = Course.objects.filter(course_name=name,semester = semester)
            if id != '' and name != '' and semester != '':
                courses = Course.objects.filter(course_id=int(id),semester = semester,course_name = name)
            if id == '' and name == '' and semester == '':
                courses = Course.objects.all()
        elif request.POST.get('input_btn') == "Your Courses":
            for secs in user.assigned_section.all():
                print(secs)
                courses.append(secs.course_parent)
        else:
            courses = Course.objects.all()
        return render(request, "courseList.html", {"courselist": courses, 'is_admin': is_admin})
