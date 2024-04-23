from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section

from ta_app.classes.SectionClass import SectionClass
class SectionView(View):

    #a = 'section_form.html'
    boo = None
    parent = Course.objects.filter().all()
    def get(self, request):
        usr_role = request.session["role"]
        #parent= Course.objects.filter().all()
        if usr_role == "Admin":
            return render(request, "create_section.html",{"courses":self.parent,"check":self.boo})
        raise Http404("MyModel does not exist")


    def post(self, request):
        course_parent = request.POST.get("course_parent", None)
        section_id = request.POST.get("section_id", None)
        meeting_time = request.POST.get("meeting_time", None)
        section_type = request.POST.get("section_type", None)

        try:
            new_section = SectionClass(course_parent, section_id, meeting_time, section_type)
            new_section.create_section()

        except ValueError:
            boo=False
            return render(request, "create_section.html",{"courses":self.parent,"check":self.boo})

        boo = True
        return render(request, "create_section.html", {"courses": self.parent, "check": self.boo})
