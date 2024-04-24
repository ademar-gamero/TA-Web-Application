
from django.shortcuts import render,redirect
from django.views import View
from ta_app.models import Course

class courseList(View):
    def get(self,request):
        courses = Course.objects.all()
        print(courses)
        return render(request,"courseList.html",{"courselist":courses}) 
    def post(self,request):
        id = request.POST.get('course_id','')
        name = request.POST.get('course_name','')
        courses = []
        if id != '' and name == '':
            courses = Course.objects.filter(course_id = int(id))
            return render(request, "courseList.html",{"courselist":courses})
        if id == '' and name != '':
            courses = Course.objects.filter(course_name = name)
            return render(request, "courseList.html",{"courselist":courses})
        return render(request,"courseList.html",{"courselist":courses}) 



















