
from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User, Day
from datetime import time

#acceptance test
class accountList(TestCase):
    green=None
    courseList=None
    accountList=None

    def setUp(self):

        self.monday = Day.objects.create(day="MO")
        self.tuesday = Day.objects.create(day="TU")
        self.wednesday = Day.objects.create(day="WE")
        self.thursday = Day.objects.create(day="TH")
        self.friday = Day.objects.create(day="FR")

        self.monday.save()
        self.tuesday.save()
        self.wednesday.save()
        self.thursday.save()
        self.friday.save()

        self.green = Client()
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
        self.teacherassistant2 = User.objects.create(
            name="tab",
            username="tab",
            password="tab",
            email="tab@email.com",
            role="Teacher-Assistant",
            phone_number=4,
            address="1",
            assigned=False
        )
        self.instructor2 = User.objects.create(name="bob", username="bob", password="instructor",
                                               email="inst@email.com", role="Instructor", phone_number=3, address="1",
                                               assigned=False)
        self.algos = Course(course_id=351, course_name="compsci", description="blah blah blah", semester="Summer")
        self.algos.save()
        self.sec = Section.objects.create(course_parent=self.algos, section_id=1, type="lecture", location="classroom")
        self.sec.save()
        self.sec2 = Section.objects.create(course_parent=self.algos, section_id=2, type="lecture", location="classroom")
        self.sec.save()
        self.accountList = [self.admin, self.instructor]

        self.lecture1 = Section.objects.create(course_parent=self.algos, section_id=101, type="LEC",
                                               start_time=time(12, 0), end_time=time(1, 30), location="class25b")

        self.lecture1.meeting_days.add(self.monday, self.wednesday)
        self.lecture1.save()

        self.lecture2 = Section.objects.create(course_parent=self.algos, section_id=205, type="LEC",
                                               start_time=time(12, 0), end_time=time(1, 30), location="class25b")

        self.lecture2.meeting_days.add(self.wednesday)
        self.lecture2.save()

        self.lab1 = Section.objects.create(course_parent=self.algos, section_id=102, type="LAB",
                                           start_time=time(11, 0), end_time=time(12, 30), location="class30B")

        self.lab1.meeting_days.add(self.thursday)
        self.lab1.save()

        self.lab2 = Section.objects.create(course_parent=self.algos, section_id=105, type="LAB",
                                           start_time=time(11, 0), end_time=time(12, 30), location="class45C")

        self.lab2.meeting_days.add(self.tuesday, self.thursday)
        self.lab2.save()

        self.detail_url_course = reverse('courseSections', args=[self.algos.pk])

        self.instructor2.assigned_section.add(self.lecture1)
        self.instructor2.save()

        self.teacherassistant.assigned_section.add(self.lecture1)
        self.teacherassistant.save()

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

    def test_searchNone(self):
        username = ''
        name = ''
        role = ''
        resp = self.green.post("/Home/accountList/", {"name": name, "username": username, "role": role}, follow=True)
        self.assertTrue(resp.context['accountlist'] == [],"search found objects it shouldnt have")

    def test_adminInvalidSearchAssignedUsers(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)
        resp = self.green.get("/Home/accountList/")
        self.assertNotContains(resp,"Show Users Assigned To Your Courses",msg_prefix="filter button should not be displayed")

    def test_searchAssignedUsers(self):
        resp = self.green.post("/login/",{"username":self.instructor2.username,"password":self.instructor2.password},follow=True)
        resp = self.green.post("/Home/accountList/",{"input_button":"Show Users Assigned To Your Courses"},follow=True)
        acc_list = [self.instructor2,self.teacherassistant]
        l = 0
        for j in resp.context["account_list"]:
            self.assertEqual(j,acc_list[l],"search did not work")
            l = l+1

