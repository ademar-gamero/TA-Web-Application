
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section, Day
from ta_app.Classes.SectionClass import SectionClass

class SectionView(View):
    template_name = 'create_section.html'

    def get(self, request):
        courses = Course.objects.all()
        sections = Section.objects.all()
        return render(request, self.template_name, {'courses': courses, 'sections': sections})

    def post(self, request):
        course_parent_id = request.POST.get("course_parent")
        section_id = request.POST.get("section_id")
        meeting_days = request.POST.getlist("days")  #  a list if checkboxes are used
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        section_type = request.POST.get("section_type")
        location = request.POST.get("location")
        is_online = request.POST.get("is_online", False) == 'on'  # Checks if online checkbox is marked
        sections = Section.objects.all()
        context = {'courses': Course.objects.all(), 'sections': sections, 'check': True}

        try:
            course_parent = Course.objects.get(id=course_parent_id)
            new_section = SectionClass(course_parent=course_parent, section_id=section_id,
                                       meeting_days=meeting_days, location=location, start_time=start_time,end_time=end_time,
                                       section_type=section_type, is_online=is_online)
            new_section.create_section()
        except Course.DoesNotExist:
            context.update({'check': False, 'error': "Course not found"})
        except ValueError as e:
            context.update({'check': False, 'error': str(e)})

        return render(request, self.template_name, context)
