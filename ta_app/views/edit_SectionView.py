from datetime import datetime

from django.views import View
from ta_app.models import Section, Course, Day, User
from ta_app.Classes.SectionClass import SectionClass
from django.shortcuts import render, redirect



class EditSectionView(View):
    section_edit = None
    section_pk = None
    val = None

    def get(self, request, pk):
        curr_acc = request.session["role"]
        days=[]
        for day in Day.objects.all():
            if day.day not in days:
                days.append(day.day)
        assignedDays= []
        for day in Section.objects.get(pk=pk).meeting_days.all():
            assignedDays.append(day.day)
        if curr_acc != "Admin":
            return redirect("/Home/")
        courses = Course.objects.all()

        section = Section.objects.get(pk=pk)
        start_time=section.start_time.strftime('%H:%M')
        end_time=section.end_time.strftime('%H:%M')
        self.section_edit = SectionClass(section.course_parent, section.section_id, section.meeting_days.all(),
                                         section.start_time, section.end_time, section.type,
                                         section.location, section.is_online)
        return render(request, "editSection.html", {'courses':courses,'section': section, 'days':days,'assignedDays':assignedDays,'start_time':start_time,'end_time':end_time,"check": self.val})

    def post(self, request, pk):
        courses = Course.objects.all()
        try:
            section = Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            return redirect('/Home/')
        daysContext = []
        for day in Day.objects.all():
            if day.day not in daysContext:
                daysContext.append(day.day)
        assignedDays = []
        for day in Section.objects.get(pk=pk).meeting_days.all():
            assignedDays.append(day.day)
        course_parent = request.POST.get('course_parent')
        course_parent= Course.objects.get(pk=course_parent)
        section_id = request.POST.get('section_id')
        start_time = request.POST.get('start_time')
        start_time=datetime.strptime(start_time, '%H:%M').strftime('%H:%M')
        end_time = request.POST.get('end_time')
        end_time=datetime.strptime(end_time, '%H:%M').strftime('%H:%M')
        section_type = request.POST.get('section_type')
        location = request.POST.get('location')
        is_online = request.POST.get('is_online')
        meeting_days = request.POST.getlist('meeting_days',None)
        if is_online != '':
            is_online = True
        else:
            is_online = False
        if meeting_days==[]:
            days=None
        else:
            days = []
            for dayss in meeting_days:
                day = Day.objects.get(day=dayss)
                days.append(day)
        try:
            oldsection = Section.objects.get(pk=pk)
            section_edit = SectionClass(course_parent=course_parent, section_id=section_id, meeting_days=days,
                                        start_time=start_time, end_time=end_time, section_type=section_type,
                                        location=location, is_online=is_online)
            section_edit.edit_section(oldsection.section_id)

        except ValueError as error:
            return render(request, "editSection.html", {'courses':courses,'section': section, 'days':daysContext,'assignedDays': assignedDays,'start_time':start_time,'end_time':end_time,'message': str(error)})
        daysContext = []
        for day in Day.objects.all():
            if day.day not in daysContext:
                daysContext.append(day.day)
        assignedDays = []
        for day in Section.objects.get(pk=pk).meeting_days.all():
            assignedDays.append(day.day)
        section=Section.objects.get(pk=pk)
        start_time = section.start_time.strftime('%H:%M')
        end_time = section.end_time.strftime('%H:%M')
        message = "Section edited successfully"
        return render(request, "editSection.html", {'courses':courses,'section': section, 'days':daysContext,'assignedDays': assignedDays,'start_time':start_time,'end_time':end_time, 'message': message})