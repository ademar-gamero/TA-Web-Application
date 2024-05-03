from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from ta_app.models import Course, Section,Day

from ta_app.Classes.SectionClass import SectionClass


class SectionView(View):
    template_name = 'create_section.html'

    def get(self, request):
        courses = Course.objects.all()
        sections = Section.objects.all()
        return render(request, 'create_section.html', {'courses': courses,'sections':sections})

    def post(self, request):
        course_parent_id = request.POST.get("course_parent")
        section_id = request.POST.get("section_id")
        meeting_days = request.POST.get("meeting_days")
        meeting_time = request.POST.get("meeting_time")
        section_type = request.POST.get("section_type")
    
        sections = Section.objects.all()
        context = {'courses': Course.objects.all(), 'sections':sections, 'check': True}  # Default context

        try:
            course_parent = Course.objects.get(id=course_parent_id)
            new_section = SectionClass(course_parent=course_parent, section_id=section_id,
                                       meeting_days=meeting_days, meeting_time=meeting_time, section_type=section_type)
            new_section.create_section()
        except Course.DoesNotExist:
            context.update({'check': False, 'error': "Course not found"})
        except ValueError as e:
            context.update({'check': False, 'error': str(e)})

        return render(request, self.template_name, context)

    def get(self, request):
        context = {'courses': Course.objects.all()}
        return render(request, self.template_name, context)
