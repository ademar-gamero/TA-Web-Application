from django.urls import reverse
from django.test import TestCase, Client
from ta_app.models import User

class home(TestCase):

    green=None

    def setUp(self):
        self.green = Client()
        User(name="admin",username="admin",password="admin",email="admin@email.com",role="Admin",phone_number=1,address="1",assigned=False).save()
        User(name="instructor",username="instructor",password="instructor",email="instructor@email.com",role="Instructor",phone_number=1,address="1",assigned=False).save()       
        self.Ausername = "admin"
        self.Apassword = "admin"
        self.Iusername = "instructor"
        self.Ipassword = "instructor"

    def test_roleValidationAdminAccountList(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertRedirects(resp,"/Home/",302,msg_prefix="redirect unsuccessful")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role validation failed")

    def test_rvAdminCorrectLinks(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertRedirects(resp,"/Home/",302,msg_prefix="redirect unsuccessful")
        resp = self.green.get('/Home/')
        self.assertContains(resp,'<a href="%s">Course Catalog</a>' % reverse("courseList"),"missing link",html=True)
        self.assertContains(resp,'<a href="%s">Create Course</a>' % reverse("createAccount"),"missing link",html=True)
        self.assertContains(resp,'<a href="%s">Account List</a>' % reverse("accountList"),"missing link",html=True)
        self.assertContains(resp,'<a href="%s">Create Account</a>' % reverse("createAccount"),"missing link",html=True)
        self.assertContains(resp,'<a href="%s">Create Section</a>' % reverse("createSection"),"missing link",html=True)




















