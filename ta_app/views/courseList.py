from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View
from ta_app.models import Course

class courseList(View):
    def get(self,request):
        courses = Course.objects.all()
        print(courses)
        return render(request,"courseList.html",{"courselist":courses}) 
    def post(self,request):
        if 'delete_course_id' in request.POST:
            course_id = request.POST.get('delete_course_id')
            course = Course.objects.filter(course_id=course_id)
            if course.exists():
                course.delete()
            else:
                messages.error(request, "Course not found.")
            return redirect('courseList')
        else:
            id = request.POST.get('course_id', '')
            name = request.POST.get('course_name', '')
            courses = Course.objects.all()
            if id:
                courses = courses.filter(course_id=int(id))
            if name:
                courses = courses.filter(course_name__icontains=name)
            return render(request, "courseList.html", {"courselist": courses})




















