from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from ta_app.models import User, Section
from django.contrib import messages

class removeSection(View):
    def get(self, request, user_id, section_id):
        if 'role' not in request.session or request.session.get('role') != 'Admin':
            messages.error(request, "You are not authorized to view this page.")
            return redirect('login')

        user = get_object_or_404(User, pk=user_id)
        section = get_object_or_404(Section, pk=section_id)
        return render(request, 'remove_section.html', {'user': user, 'section': section})

    def post(self, request, user_id, section_id):
        if 'role' in request.session and request.session['role'] == 'Admin':
            user = get_object_or_404(User, pk=user_id)
            section = get_object_or_404(Section, pk=section_id)
            if 'confirm' in request.POST:
                user.assigned_section.remove(section)
                messages.success(request, f'{user.name} removed from section {section}')
            else:
                messages.warning(request, 'Removal not confirmed.')
            return redirect('accountAssignment', pk=user_id)
        else:
            messages.error(request, "Unauthorized attempt to remove section assignment.")
            return redirect('login')
