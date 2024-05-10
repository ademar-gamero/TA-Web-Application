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
            tas = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section]).distinct()
            for ta in tas:
                if ta not in ta_pool:
                    ta_pool.append(ta)
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

        for section in sections:
            tas = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section]).distinct()
            for ta in tas:
                if ta not in ta_pool:
                    ta_pool.append(ta)

        dict = {}
        for key,values in request.POST.lists():
            if key != "csrfmiddlewaretoken":
                if key in dict:
                    dict[key].extend(values)
                else:
                    dict[key] = values
        print(dict)
        assigned = False
        for key, value in dict.items():
            for val in value:
                if val != 'None':
                    try:
                        acc = User.objects.get(pk=val)
                        sec = Section.objects.get(pk=key)
                        newacc = UserClass(username=acc.username, password=acc.password, name=acc.name, role=acc.role,
                                           email=acc.email,
                                           phone_number=acc.phone_number, address=acc.address, assigned=acc.assigned,
                                           assigned_sections=acc.assigned_section.all())
                        newacc.add_section(sec)
                        assigned = True

                    except ValueError as failure:
                        return render(request, "course_sections.html", {"course": course, "sections": sections,
                                                                        "ta_all": teacherassistant_pool,
                                                                        "ins_all": instructor_pool, "usr_role": usr_role,
                                                                        "ta_pool": ta_pool, "message": failure.__str__()})

        course = Course.objects.get(pk=course_pk)
        sections = Section.objects.filter(course_parent=course)
        ta_pool = []

        for section in sections:
            tas = User.objects.filter(role="Teacher-Assistant", assigned_section__in=[section]).distinct()
            for ta in tas:
                if ta not in ta_pool:
                    ta_pool.append(ta)

        success = "Nothing was Submitted"
        if assigned:
            success = "Successfully assigned user(s) to section"

        return render(request, "course_sections.html", {"course": course, "sections": sections,
                                                        "ta_all": teacherassistant_pool, "ins_all": instructor_pool,
                                                        "usr_role": usr_role, "ta_pool": ta_pool, "message": success})





