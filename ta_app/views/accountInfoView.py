from django.contrib import messages
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.views import View
from ta_app.models import User
from ta_app.Classes.UserClass import UserClass
from django.shortcuts import redirect


class accountInfoView(View):
    acc_edit = None
    acc_pk = None
    val = None

    def get(self,request,pk):
        roles = ["Admin","Instructor","Teacher-Assistant"]
        if 'role' not in request.session or 'name' not in request.session:
            messages.error(request, "You are not logged in.")
            return redirect('login')
        curr_acc = request.session["role"]
        is_admin = False
        own_acc = False
        if curr_acc == "Admin":
            is_admin = True
        elif request.session["pk"] != pk:
            return redirect("/Home/")
        if request.session["pk"] == pk:
            own_acc = True
        account = User.objects.get(pk=pk)
        self.acc_edit = UserClass(username=account.username, password=account.password, name=account.name, role=account.role,
                                  email=account.email, phone_number=account.phone_number, address=account.address, assigned=account.assigned,
                                  assigned_sections=account.assigned_section.all(), skills=account.skills)
        return render(request, "accountInfo.html", {'user': account, 'is_admin': is_admin,"roles":roles, "own_acc":own_acc})

    def post(self, request, pk):
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')
        address = request.POST.get('address')

        self.val = False
        account = User.objects.get(pk=pk)
        self.acc_edit = UserClass(username=account.username, password=account.password, name=account.name, role=account.role,
                                  email=account.email, phone_number=account.phone_number, address=account.address, assigned=account.assigned,
                                  assigned_sections=account.assigned_section.all(), skills=account.skills)
        try:
            self.acc_edit.edit_user(username=username, password=password, name=name, role=role, email=email,
                                    phone=phone_number, address=address)
        except ValueError as error:
            return render(request, "accountInfo.html", {'user': self.acc_edit, 'message': error.__str__()})
        updated_account = User.objects.get(pk=pk)
        return render(request, "accountInfo.html", {'user': updated_account,
                                                    'message': f'Account \'{updated_account.username}\' edited successfully!'})
