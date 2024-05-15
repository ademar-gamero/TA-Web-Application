
from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User
from datetime import datetime


class editAccount(TestCase):
    def setUp(self):
        self.green = Client()
        self.courselist = {351: ["compsci", "this course covers algos and data structs"],
                      361: ["compsci", "this course covers software engineering"],
                      102: ["psych", "this course covers psychology"]}
        self.admin = User.objects.create(
                name="ad",
                username="admin",
                password="admin",
                email="admin@email.com",
                role="Admin",
                phone_number=1,
                address="1",
                assigned=False
                )
        self.admin.save()
        self.instructor = User.objects.create(
                name="inst",
                username="instructor",
                password="instructor",
                email="instructor@email.com",
                role="Instructor",
                phone_number=2,
                address="1",
                assigned=False
                )
        self.instructor.save()
        self.teacherassistant = User.objects.create(
                name="ta",
                username="ta",
                password="ta",
                email="ta@email.com",
                role="Teacher-Assistant",
                phone_number=4,
                address="1",
                assigned=False
                )
        self.teacherassistant.save()
        self.instructor2 = User.objects.create(name="bob",username="bob",password="instructor",email="inst@email.com",role="Instructor",phone_number=3,address="1",assigned=False)
        self.Ausername = "admin"
        self.Apassword = "admin"
        self.Iusername = "instructor"
        self.Ipassword = "instructor"
        self.algos = Course(course_id=351,course_name="compsci",description="blah blah blah",semester="Summer")
        self.algos.save()
        date_str = "Tue 2:30pm"
        date = datetime.strptime(date_str,"%a %I:%M%p")
        self.sec = Section(course_parent = self.algos,section_id=1,type="lecture",location="classroom")
        self.sec.save()
        self.accountList = [self.admin,self.instructor]
        self.detail_url = reverse('accountInfo',args=[self.instructor.pk])
        self.instructor2.assigned_section.add(self.sec)
        self.instructor2.save()

    def test_validAccessEditAcc(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

    def test_invalidInstructorAccessEditAcc(self):
        resp = self.green.post("/login/",{"username":self.instructor.username,"password":self.instructor.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"account list web page not setup properly")
        resp = self.green.get(self.detail_url)
        self.assertEqual(302,resp.status_code,"role validation failed")
        self.assertRedirects(resp, "/Home/", msg_prefix="did not redirect")

    def test_invalidTeacherAssistantAccessEditAcc(self):
        resp = self.green.post("/login/",{"username":self.teacherassistant.username,"password":self.teacherassistant.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"account list web page not setup properly")
        resp = self.green.get(self.detail_url)
        self.assertEqual(302,resp.status_code,"role validation failed")
        self.assertRedirects(resp, "/Home/", msg_prefix="did not redirect")

    def test_editName(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {
            "name":"felix",
            "username":self.admin.username,
            "email":self.admin.email,
            "password":self.admin.password,
            "phone_number":self.admin.phone_number,
            "role":self.admin.role,
            "address":self.admin.address,
            }, follow=True)

        self.assertTrue(resp.context['message'], "Account admin edited successfully!")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(new.name == "felix", "name was not edited")

    def test_editUserName(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {"username":"felix"} ,follow=True)
        self.assertTrue(resp.context['message'],"Account admin edited successfully!",msg_prefix="message was not displayed")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(new.username == "felix","username was not edited")

    def test_editInvalidUserName(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {"username":"ta"} ,follow=True)
        self.assertTrue(resp.context['message'],"Username 'ta' taken please enter a different username", msg_prefix="message was not displayed")
        self.assertTrue(self.instructor.username == "instructor","username was edited when it shouldnt have been")


    def test_editPassword(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {"password":"Mr.Robot"} ,follow=True)
        self.assertTrue(resp.context['message'],"Account instructor edited successfully!",msg_prefix="message was not displayed")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(new.password == "Mr.Robot","password was not edited")
        
    def test_editRole(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {"role":self.ta.role} ,follow=True)
        self.assertTrue(resp.context['message'],"Account instructor edited successfully!",msg_prefix="message was not displayed")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(new.role == self.ta.role,"role was not edited")


    def test_editPhoneNumber(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {"phone_number":"371-121-121"} ,follow=True)
        self.assertTrue(resp.context['message'],"Account instructor edited successfully!",msg_prefix="message was not displayed")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(new.phone_number == "371-121-121","phone_number was not edited")

    def test_editEmail(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {"email":"newgrounds@email.com"} ,follow=True)
        self.assertTrue(resp.context['message'],"Account instructor edited successfully!",msg_prefix="message was not displayed")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(new.email == "newgrounds@email.com","email was not edited")


    def test_editInvalidEmail(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url, {"email":self.ta.email} ,follow=True)
        self.assertTrue(resp.context['message'],"Duplicate email entered, can not be edited",msg_prefix = "message was not displayed")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(new.email != self.ta.email,"email was not edited")

## tests below need adjustment




