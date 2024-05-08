
from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User
from datetime import time


class accountAssignment(TestCase):
    def setUp(self):
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
                name="ta",
                username="tab",
                password="tab",
                email="tab@email.com",
                role="Teacher-Assistant",
                phone_number=4,
                address="1",
                assigned=False
                )
        self.instructor2 = User.objects.create(name="bob",username="bob",password="instructor",email="inst@email.com",role="Instructor",phone_number=3,address="1",assigned=False)
        self.Ausername = "admin"
        self.Apassword = "admin"
        self.Iusername = "instructor"
        self.Ipassword = "instructor"
        self.algos = Course(course_id=351,course_name="compsci",description="blah blah blah",semester="Summer")
        self.algos.save()
        date_str = "Tue 2:30pm"
        self.sec = Section.objects.create(course_parent = self.algos,section_id=1,type="lecture",location="classroom")
        self.sec.save()
        self.sec2 = Section.objects.create(course_parent = self.algos,section_id=2,type="lecture",location="classroom")
        self.sec.save()
        self.accountList = [self.admin,self.instructor]

        self.lecture1 = Section.objects.create(course_parent=self.algos, section_id=101, type="LEC",
                                               start_time=time(12, 0), end_time=time(1, 30),
                                               meeting_days=["TU", "TH"],location="class25b")

        self.lecture2 = Section.objects.create(course_parent=self.algos, section_id=205, type="LEC",
                                               start_time=time(12, 0), end_time=time(1, 30),
                                               meeting_days=["TH"],location="class25b")

        self.lab1 = Section.objects.create(course_parent=self.algos, section_id=102, type="LAB",
                                               start_time=time(11, 0), end_time=time(12, 30),
                                               meeting_days=["MO", "WE"],location="class30B")

        self.detail_url_course = reverse('courseSections',args=[self.algos.pk])

        self.instructor2.assigned_section.add(self.lecture1)
        self.instructor2.save()

        self.teacherassistant2.assigned_section(self.lecture1)
        self.teacherassistant2.save()

    def test_adminAccess(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")

    def test_instructorAccess(self):
        resp = self.green.post("/login/",{"username":self.instructor.username,"password":self.instructor.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")

    def test_taAccess(self):
        resp = self.green.post("/login/",{"username":self.ta.username,"password":self.ta.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")

    def test_taAddViewCheck(self):
        resp = self.green.post("/login/",{"username":self.ta.username,"password":self.ta.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"Add User",msg_prefix="Ta shouldnt be able to add users")

    def test_taDeleteViewCheck(self):
        resp = self.green.post("/login/",{"username":self.ta.username,"password":self.ta.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"delete link",msg_prefix="Ta shouldnt be able Remove a Section")

    def test_taRemoveAssignmentViewCheck(self):
        resp = self.green.post("/login/",{"username":self.ta.username,"password":self.ta.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"Remove Assignment",msg_prefix="Ta shouldnt be able to add users")

    def test_adminAssignUser(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.green.post(self.detail_url_course, {self.lab1.pk:self.teacherassistant.id},follow=True)
        updated_section = Section.objects.get(pk=self.lab1.pk)
        self.assertIn(updated_section.assigned_users,self.teacherassistant,"user was not assigned to the section")

    def test_instructorAssignUser(self):
        resp = self.green.post("/login/",{"username":self.instructor2.username,"password":self.instructor2.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.green.post(self.detail_url_course, {self.lab1.pk:self.teacherassistant2.id},follow=True)
        updated_section = Section.objects.get(pk=self.lab1.pk)
        self.assertIn(updated_section.assigned_users,self.teacherassistant2,"user was not assigned to the section")

    def test_instructorInvalidAssignUser(self):
        resp = self.green.post("/login/",{"username":self.instructor2.username,"password":self.instructor2.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.green.post(self.detail_url_course, {self.lab1.pk:self.teacherassistant.id},follow=True)
        updated_section = Section.objects.get(pk=self.lab1.pk)
        self.assertNotIn(updated_section.assigned_users,self.teacherassistant,"user shouldn't have been assigned")
