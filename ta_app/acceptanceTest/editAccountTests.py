
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
        self.admin = User(name="ad",username="admin",password="admin",email="admin@email.com",role="Admin",phone_number=1,address="1",assigned=False)
        self.admin.save()
        self.instructor = User(name="inst",username="instructor",password="instructor",email="instructor@email.com",role="Instructor",phone_number=2,address="1",assigned=False)
        self.instructor2 = User.objects.create(name="bob",username="instructor",password="instructor",email="inst@email.com",role="Instructor",phone_number=3,address="1",assigned=False)
        self.instructor.save()
        self.Ausername = "admin"
        self.Apassword = "admin"
        self.Iusername = "instructor"
        self.Ipassword = "instructor"
        self.algos = Course(course_id=351,course_name="compsci",description="blah blah blah")
        self.algos.save()
        date_str = "Tue 2:30pm"
        date = datetime.strptime(date_str,"%a %I:%M%p")
        self.sec = Section(course_parent = self.algos,section_id=1,meeting_time=date,type="lecture")
        self.sec.save()
        self.accountList = [self.admin,self.instructor]
        self.detail_url = reverse('accountDetails',args=[self.instructor.id])
        self.instructor2.assigned_section.add(self.sec)
        self.instructor2.save()

    def test_accessEditAcc(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

    def test_editName(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        form = {
        'name': 'chairman',  
        'username': resp.context['user.username'],
        'email': resp.context['user.email'],
        'password': resp.context['user.password'],
        'phone_number': resp.context['user.phone_number'],
        'role': resp.context['user.role'],  
        }
        
        resp = self.green.post(self.detail_url, form ,follow=True)
        self.assertContains(resp, f'value="{form["name"]}"',"value did not update")
        self.assertTrue(resp.context['check'],"bool val is False when should be True")

    def test_editNameIncorrect(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"username":self.instructor2.username},follow=True)
        self.assertFalse(resp.context['check'],"user was updated to contain invalid duplicated information")
        self.assertContains(resp, f'value="{self.admin.username}"',"value updated when it shoulnt have")

    def test_editRole(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"role":self.instructor2.role},follow=True)
        self.assertTrue(resp.context['check'],"bool val is False when should be True")
        self.assertContains(resp, f'value="{self.instructor2.role}"',"value did not update in html")

    def test_editAssigned(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"assigned":self.instructor2.assigned},follow=True)
        self.assertTrue(resp.context['check'],"bool val is False when should be True")
        self.assertContains(resp, f'value="{self.instructor2.assigned}"',"value did not update in html")


    def test_editInValidPhoneNumber(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"phone_number":self.instructor2.phone_number},follow=True)
        self.assertContains(resp,"Phone Number: "+self.instructor2.phone_number)
        self.assertFalse(resp.context['check'],"user was updated to contain invalid duplicated information")
        self.assertContains(resp, f'value="{self.admin.phone_number}"',"value updated when it shouldnt have ")

    def test_editEmail(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"email":"cryptic@email.com"},follow=True)
        self.assertTrue(resp.context['check'],"bool val is False when should be True")
        self.assertContains(resp, f'value="{"cryptic@email.com"}"',"value did not update in html")

    def test_editInvalidEmail(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"email":self.instructor2.email},follow=True)
        self.assertFalse(resp.context['check'],"user was updated to contain invalid duplicated information")
        self.assertContains(resp, f'value="{self.admin.email}"',"value updated when it shouldnt have ")

    def test_editPassword(self): 
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"password":self.instructor2.password},follow=True)
        self.assertTrue(resp.context['check'],"bool val is False when should be True")
        self.assertContains(resp, f'value="{self.instructor2.password}"',"value did not update in html")

    def test_sameEditPhoneNumber(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"phone_number":1},follow=True)
        self.assertTrue(resp.context['check'],"bool val is False when should be True")
        self.assertContains(resp, f'value="{"1"}"',"value did not update in html")

        

        
        

        

        
        

        

        
        

        
        
