
from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User
from datetime import datetime

#acceptance test
class accountList(TestCase):
    green=None
    courseList=None
    accountList=None
    def setUp(self):
        self.green = Client()
        self.courselist = {351: ["compsci", "this course covers algos and data structs"],
                      361: ["compsci", "this course covers software engineering"],
                      102: ["psych", "this course covers psychology"]}


        self.admin = User(name="ad",username="admin",password="admin",email="admin@email.com",role="Admin",phone_number=1,address="1",assigned=False)
        self.admin.save()
        self.instructor = User(name="inst",username="instructor",password="instructor",email="instructor@email.com",role="Instructor",phone_number=2,address="1",assigned=False)
        self.instructor2 = User(name="bob",username="instructor",password="instructor",email="inst@email.com",role="Instructor",phone_number=3,address="1",assigned=False)
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

    def test_access(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role validation failed")
        
    def test_displayAccounts(self):
        resp = self.green.get("/Home/accountList/")
        for j in resp.context["accountlist"]:
            self.assertIn(j,self.accountList,"not all accounts are listed")

    def test_searchCorrectName(self):
        name = self.instructor.name
        resp = self.green.post("/Home/accountList/",{"name":name},follow=True)
        for j in resp.context["accountlist"]:
            self.assertEqual(j.name,name,"search shouldve found a course id but didnt")

    def test_searchIncorrectCourseID(self):
        name = "Quentin Tarantino"
        resp = self.green.post("/Home/accountList/",{"name":name},follow=True)

        clist = resp.context["accountlist"]
        checker = False
        if len(clist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")

    def test_searchAccountUserName(self):
        username = self.Iusername
        resp = self.green.post("/Home/accountList/",{"username":username},follow=True)
        for j in resp.context["accountlist"]:
            self.assertEqual(j.username,username,"search is not working")

    def test_searchIncorrectUserName(self):
        username = "Teacher_Assistant" 
        resp = self.green.post("/Home/accountList/",{"username":username},follow=True)
        alist = resp.context["accountlist"]
        checker = False
        if len(alist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")

    def test_searchAccountRole(self):
        role = self.instructor.role
        resp = self.green.post("/Home/accountList/",{"role":role},follow=True)
        for j in resp.context["accountlist"]:
            self.assertEqual(j.role,role,"search is not working")
            
    def test_searchIncorrectAccountRole(self):
        role = "Teacher-Assistant"
        print(role)
        resp = self.green.post("/Home/accountList/",{"role":role},follow=True)
        alist = resp.context["accountlist"]
        checker = False
        if len(alist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")

    def test_searchNameRole(self):
        name = self.instructor.name
        role = self.instructor.role
        resp = self.green.post("/Home/accountList/",{"name":name,"role":role},follow=True)
        for j in resp.context["accountlist"]:
            self.assertEqual(j.role,role,"search did not work")
            self.assertEqual(j.name,name,"search did not work")

    def test_searchUserNameRole(self):
        username = self.instructor.username
        role = self.instructor.role
        resp = self.green.post("/Home/accountList/",{"username":username,"role":role},follow=True)
        for j in resp.context["accountlist"]:
            self.assertEqual(j.role,role,"search did not work")
            self.assertEqual(j.username,username,"search did not work")

    def test_searchUsernameName(self):
        username = self.instructor.username
        name = self.instructor.name
        resp = self.green.post("/Home/accountList/",{"username":username,"name":name},follow=True)
        for j in resp.context["accountlist"]:
            self.assertEqual(j.username,username,"search did not work")
            self.assertEqual(j.name,name,"search did not work")

    def test_searchUserNameRoleThree(self):
        username = self.instructor.username
        name = self.instructor.name
        role = self.instructor.role
        resp = self.green.post("/Home/accountList/",{"name":name,"username":username,"role":role},follow=True)
        for j in resp.context["accountlist"]:
            self.assertEqual(j.name,name,"search did not work")
            self.assertEqual(j.username,username,"search did not work")
            self.assertEqual(j.role,role,"search did not work")

