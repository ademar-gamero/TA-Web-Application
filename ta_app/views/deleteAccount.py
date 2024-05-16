from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ta_app.models import User
from django.contrib import messages
from ta_app.Classes.UserClass import UserClass

class deleteAccount(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # Ensure user is fetched properly
        if 'role' not in request.session or request.session.get('role') != 'Admin':
            messages.error(request, "You are not authorized to view this page.")
            return redirect('login')
        return render(request, 'delete_account.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if 'confirm' in request.POST:
            deleted = UserClass(username=user.username, password=user.password, name=user.name, role=user.role,
                                email=user.email, address=user.address, phone_number=user.phone_number,
                                skills=user.skills, assigned=user.assigned, assigned_sections=list(user.assigned_section.all()))
            try:
                deleted.delete_user()
                messages.success(request, 'Account deleted successfully!')
            except ValueError as e:
                messages.error(request, e.__str__())
            return redirect('accountList')
        return render(request, 'delete_account.html', {'user': user})