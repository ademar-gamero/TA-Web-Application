from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ta_app.models import Section
from django.contrib import messages

class deleteSection(View):
    def get(self, request, pk):
        if 'role' not in request.session or request.session.get('role') != 'Admin':
            messages.error(request, "You are not authorized to view this page.")
            return redirect('login')

        section = get_object_or_404(Section, pk=pk)
        return render(request, 'delete_section.html', {'section': section})

    def post(self, request, pk):
        if 'role' in request.session and request.session['role'] == 'Admin':
            section = get_object_or_404(Section, pk=pk)
            if 'confirm' in request.POST:
                section.delete()
                messages.success(request, 'Section deleted successfully!')
                return redirect('courseList')
            else:
                messages.warning(request, 'Please confirm deletion.')
                return render(request, 'delete_section.html', {'section': section})
        else:
            messages.error(request, "Unauthorized attempt to delete a section.")
            return redirect('login')
