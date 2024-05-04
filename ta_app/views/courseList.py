from django.shortcuts import render, redirect
from django.views import View
from ta_app.models import Course
from django.contrib import messages

class courseList(View):
    def get(self, request):
        courses = Course.objects.all()
        is_admin = request.session.get('role') == 'Admin'  # Check if user is an admin
        return render(request, "courseList.html", {"courselist": courses, "is_admin": is_admin})

    def post(self, request):
        is_admin = request.session.get('role') == 'Admin'  # Check if user is an admin
        id = request.POST.get('course_id','')
        name = request.POST.get('course_name','')
        semester = request.POST.get('semesters','')
        courses = []
        if id != '' and name == '' and semester == '':
            courses = Course.objects.filter(course_id = int(id))
            return render(request,"courseList.html",{"courselist":courses,'is_admin':is_admin}) 
        if id == '' and name != '' and semester == '':
            courses = Course.objects.filter(course_name = name)
            return render(request,"courseList.html",{"courselist":courses,'is_admin':is_admin }) 
        if id == '' and name == '' and semester != '':
            courses = Course.objects.filter(semester = semester)
            return render(request,"courseList.html",{"courselist":courses,'is_admin':is_admin}) 
        if id != '' and name != '' and semester == '':
            courses = Course.objects.filter(course_id=id,course_name = name)
            return render(request,"courseList.html",{"courselist":courses,'is_admin':is_admin}) 
        if id != '' and name == '' and semester != '':
            courses = Course.objects.filter(course_id=id,semester = semester)
            return render(request,"courseList.html",{"courselist":courses,'is_admin':is_admin}) 
        if id != '' and name != '' and semester != '':
            courses = Course.objects.filter(course_id=id,semester = semester,course_name = name)
            return render(request,"courseList.html",{"courselist":courses,'is_admin':is_admin}) 
