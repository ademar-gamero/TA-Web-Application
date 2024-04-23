
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

    def test_accessInvalidAcc(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        detail_url = reverse('accountDetails',args=[45])
        resp = self.green.get(self.detail_url)
        self.assertEqual(400,resp.status_code,"page was not displayed")

    def test_editName(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"name":self.instructor2.name},follow=True)
        self.assertContains(resp,"Name: "+self.instructor2.name)

    def test_editDuplicateUserName(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"username":self.instructor2.username},follow=True)
        self.assertContains(resp,"Name: "+self.admin.username)

    def test_editDuplicateUserName(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"username":"chairman"},follow=True)
        self.assertContains(resp,"Name: " + "chairman")

    def test_editRole(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"role":self.instructor2.role},follow=True)
        self.assertContains(resp,"Role: "+self.instructor2.role)

    def test_editAssigned(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"assigned":self.instructor2.assigned},follow=True)
        self.assertContains(resp,"Assigned: "+self.instructor2.assigned)

    def test_editAssignedSections(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url,{"Assigned Sections":self.instructor2.assigned_section},follow=True)
        self.assertContains(resp,"Assigned Sections: "+self.instructor2.assigned_section.all())

    def test_editPhoneNumber(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"phone_number":self.instructor2.phone_number},follow=True)
        self.assertContains(resp,"Phone Number: "+self.instructor2.role)

    def test_editEmail(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"email":"cryptic@email.com"},follow=True)
        self.assertContains(resp,"Email: "+ "cryptic@email.com")

    def test_editInvalidEmail(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"email":self.instructor2.email},follow=True)
        self.assertContains(resp,"Email: "+self.admin.email)

    def test_editPassword(self): 
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"password":self.instructor2.password},follow=True)
        self.assertContains(resp,"password: "+self.instructor2.password)

    def test_sameEditPhoneNumber(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/',"incorrect redirect")
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail.url,{"phone_number":1},follow=True)
        self.assertContains(resp,"Phone Number: "+self.admin.phone_number)

        

        
        

        

        
        

        

        
        

        
        
