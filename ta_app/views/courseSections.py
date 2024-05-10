from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section, User
from ta_app.Classes.UserClass import UserClass


class courseSections(View):

    def get(self, request, course_pk):
        usr_role = request.session["role"]
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent=course)
        teacherassistant_pool = User.objects.filter(role="Teacher-Assistant")
        instructor_pool = User.objects.filter(role="Instructor")

        ta_pool = []
        for section in sections:
            ta = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section])
            for tas in ta:
                ta_pool.append(tas)
        return render(request, "course_sections.html", {"course": course, "sections": sections,
                                                        "ta_all": teacherassistant_pool, "ins_all": instructor_pool,
                                                        "usr_role": usr_role, "ta_pool": ta_pool})

    def post(self, request, course_pk):
        usr_role = request.session["role"]
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent=course)
        teacherassistant_pool = User.objects.filter(role="Teacher-Assistant")
        instructor_pool = User.objects.filter(role="Instructor")
        ta_pool = []

        course = Course.objects.get(pk=course_pk)
        for key, value in request.POST.items():

            try:

                acc = User.objects.get(pk=value)
                sec = Section.objects.get(pk=key)

                newacc = UserClass(username=acc.username, password=acc.password, name=acc.name, role=acc.role,
                                   email=acc.email,
                                   phone_number=acc.phone_number, address=acc.address, assigned=acc.assigned,
                                   assigned_sections=acc.assigned_section.all())
                newacc.add_section(sec)

            except ValueError as failure:
                return render(request, "course_sections.html", {"course": course, "sections": sections,
                                                                "ta_all": teacherassistant_pool,
                                                                "ins_all": instructor_pool, "usr_role": usr_role,
                                                                "ta_pool": ta_pool, "message": failure})

        usr_role = request.session["role"]
        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent=course)
        teacherassistant_pool = User.objects.filter(role="Teacher-Assistant")
        instructor_pool = User.objects.filter(role="Instructor")
        ta_pool = []

        for section in sections:
            ta = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section])
            for tas in ta:
                ta_pool.append(tas)
        success = "Successfully assigned user to section"
        return render(request, "course_sections.html", {"course": course, "sections": sections,
                                                        "ta_all": teacherassistant_pool, "ins_all": instructor_pool,
                                                        "usr_role": usr_role, "ta_pool": ta_pool, "message": success})





