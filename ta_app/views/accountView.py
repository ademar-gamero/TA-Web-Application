
from django.shortcuts import render
from django.views import View
from ta_app.models import User
from ta_app.Classes.UserClass import UserClass

class accountView(View):
    acc_edit = None
    acc_pk = None
    val = None
    def get(self,request,pk):
        self.acc_pk = pk
        account = User.objects.get(pk=self.acc_pk) 
        self.acc_edit = UserClass(account.username,account.password,account.name,account.role,
        account.email,account.phone_number,account.address,account.assigned,account.assigned_section)
        return render(request,"courseList.html",{'user': account,"check":self.val})

    def post(self,request,pk):
        name = request.POST.get('name')    
        username = request.POST.get('username')    
        email = request.POST.get('email')    
        password = request.POST.get('password')    
        phone_number = request.POST.get('phone_number')    
        role = request.POST.get('role')    
        address = request.POST.get('address')

        self.val = False
        account = User.objects.get(pk=self.acc_pk)
        self.acc_edit = UserClass(account.username, account.password, account.name, account.role,
                                  account.email, account.phone_number, account.address, account.assigned,
                                  account.assigned_section)
        try:
            self.acc_edit.edit_user(username=username,password=password,name=name,role=role,email=email,phone=phone_number,address=address)
        except ValueError:
            return render(request,"courseList.html",{'user': self.acc_edit,'check':self.val})
        self.val = True
        updated_acc = User.objects.get(pk=self.acc_pk)
        return render(request,"courseList.html",{'user': updated_acc, 'check':self.val })

            
