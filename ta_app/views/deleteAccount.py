from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from ta_app.models import User
from django.contrib import messages

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
            user.delete()
            messages.success(request, 'Account deleted successfully!')
            return redirect('accountList')
        return render(request, 'delete_account.html', {'user': user})