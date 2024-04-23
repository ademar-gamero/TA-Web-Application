
from django.shortcuts import render,redirect
from django.views import View
from ta_app.models import Course,User
from django.http import Http404

class accountList(View):
    def get(self,request):
        accounts = User.objects.all()
        return render(request,"accountList.html",{"accountlist":accounts})
    def post(self,request):

         name = request.POST.get('name','')
         username = request.POST.get('username','')
         role = request.POST.get('role','')

         if name != '' and username != '' and role !='':
            accounts = User.objects.filter(name = name,username=username,role=role)
            return render(request,"accountList.html",{"accountlist":accounts})
         if name != '' and username != '' and role =='':
            accounts = User.objects.filter(name = name,username=username)
            return render(request,"accountList.html",{"accountlist":accounts})
         if name != '' and username == '' and role !='':
            accounts = User.objects.filter(name = name,role=role)
            return render(request,"accountList.html",{"accountlist":accounts})
         if name == '' and username != '' and role !='':
            accounts = User.objects.filter(username=username,role=role)
            return render(request,"accountList.html",{"accountlist":accounts})
         if name == '' and username == '' and role !='':
            accounts = User.objects.filter(role=role)
            return render(request,"accountList.html",{"accountlist":accounts})
         if name == '' and username != '' and role =='':
            accounts = User.objects.filter(username=username)
            return render(request,"accountList.html",{"accountlist":accounts})
         if name != '' and username == '' and role =='':
            accounts = User.objects.filter(name=name)
            return render(request,"accountList.html",{"accountlist":accounts})
























