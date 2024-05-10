
from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User, Day
from datetime import time


class accountAssignment(TestCase):
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
        self.instructor2 = User.objects.create(name="bob",username="bob",password="instructor",email="inst@email.com",role="Instructor",phone_number=3,address="1",assigned=False)
        self.algos = Course(course_id=351,course_name="compsci",description="blah blah blah",semester="Summer")
        self.algos.save()
        self.sec = Section.objects.create(course_parent = self.algos,section_id=1,type="lecture",location="classroom")
        self.sec.save()
        self.sec2 = Section.objects.create(course_parent = self.algos,section_id=2,type="lecture",location="classroom")
        self.sec.save()
        self.accountList = [self.admin,self.instructor]

        self.lecture1 = Section.objects.create(course_parent=self.algos, section_id=101, type="LEC",
                                               start_time=time(12, 0), end_time=time(1, 30), location="class25b")

        self.lecture1.meeting_days.add(self.monday, self.wednesday)
        self.lecture1.save()

        self.lecture2 = Section.objects.create(course_parent=self.algos, section_id=205, type="LEC",
                                               start_time=time(12, 0), end_time=time(1, 30),location="class25b")

        self.lecture2.meeting_days.add(self.wednesday)
        self.lecture2.save()

        self.lab1 = Section.objects.create(course_parent=self.algos, section_id=101, type="LAB",
                                               start_time=time(11, 0), end_time=time(12, 30),location="class30B")

        self.lab1.meeting_days.add(self.thursday)
        self.lab1.save()

        self.lab2 = Section.objects.create(course_parent=self.algos, section_id=102, type="LAB",
                                           start_time=time(11, 0), end_time=time(12, 30), location="class45C")

        self.lab2.meeting_days.add(self.tuesday,self.thursday)
        self.lab2.save()

        self.lab3 = Section.objects.create(course_parent=self.algos, section_id=103, type="LAB",
                                           start_time=time(11, 0), end_time=time(12, 30), location="class46C")

        self.lab3.meeting_days.add(self.thursday)
        self.lab3.save()


        self.detail_url_course = reverse('courseSections',args=[self.algos.pk])

        self.instructor2.assigned_section.add(self.lecture1)
        self.instructor2.save()

        self.teacherassistant.assigned_section.add(self.lecture1)
        self.teacherassistant.save()

    def test_adminAccess(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)
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
        resp = self.green.post("/login/",{"username":self.teacherassistant.username,"password":self.teacherassistant.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")

    def test_taAddViewCheck(self):
        resp = self.green.post("/login/",{"username":self.teacherassistant.username,"password":self.teacherassistant.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"Add User",msg_prefix="Ta shouldnt be able to add users")

    def test_taDeleteViewCheck(self):
        resp = self.green.post("/login/",{"username":self.teacherassistant.username,"password":self.teacherassistant.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"delete link",msg_prefix="Ta shouldnt be able Remove a Section")

    def test_taRemoveAssignmentViewCheck(self):
        resp = self.green.post("/login/",{"username":self.teacherassistant.username,"password":self.teacherassistant.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"Remove Assignment",msg_prefix="Ta shouldnt be able to add users")

    def test_adminAssignValidInSideLecture(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url_course, {self.lab1.pk:self.teacherassistant.pk},follow=True)
        self.assertContains(resp, "Successfully assigned user(s) to section(s)",
                            msg_prefix="message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lab1.pk)
        self.assertIn(self.teacherassistant,updated_section.assigned_users.all(),"user was not assigned to the section")

    def test_adminAssignValidOutSideLecture(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url_course, {self.lecture2.pk:self.teacherassistant2.pk},follow=True)
        self.assertContains(resp, "Successfully assigned user(s) to section(s)",
                            msg_prefix="message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lecture2.pk)
        self.assertIn(self.teacherassistant2,updated_section.assigned_users.all(),"user was not assigned to the section")

    def test_adminAssignInValidLabOutSideLecture(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url_course, {self.lab1.pk:self.teacherassistant2.pk},follow=True)
        self.assertContains(resp, "User is not assigned to a corresponding lecture section in this course",
                            msg_prefix="message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lab1.pk)
        self.assertNotIn(self.teacherassistant2,updated_section.assigned_users.all(),"user was not assigned to the section")

    def test_adminAssignConflictingSections(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url_course, {self.lecture2.pk:self.teacherassistant2.pk},follow=True)
        self.assertContains(resp, "Successfully assigned user(s) to section(s)",
                            msg_prefix="message was not printed to the user")
        resp = self.green.post(self.detail_url_course, {self.lab2.pk:self.teacherassistant2.pk},follow=True)
        self.assertContains(resp, "Successfully assigned user(s) to section(s)",
                            msg_prefix="message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lab2.pk)
        self.assertIn(self.teacherassistant2,updated_section.assigned_users.all(),"user was not assigned to the section")
        resp = self.green.post(self.detail_url_course, {self.lab3.pk:self.teacherassistant2.pk},follow=True)
        self.assertContains(resp,"The section being assigned conflicts with another section assignment :",msg_prefix="error message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lab3.pk)
        self.assertNotIn(self.teacherassistant2,updated_section.assigned_users.all(),"user should have been assigned")

    def test_instructorLabInvalidAssignUser(self):
        resp = self.green.post("/login/",{"username":self.instructor2.username,"password":self.instructor2.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url_course, {self.lab1.pk:self.teacherassistant2.pk},follow=True)
        self.assertContains(resp,"User is not assigned to a corresponding lecture section in this course",msg_prefix="error message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lab1.pk)
        self.assertNotIn(self.teacherassistant2,updated_section.assigned_users.all(),"user should have been assigned")

    def test_instructorLectureInvalidAssignUser(self):
        resp = self.green.post("/login/",{"username":self.instructor2.username,"password":self.instructor2.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url_course, {self.lecture2.pk:self.teacherassistant2.pk},follow=True)
        self.assertNotContains(resp,"User is not assigned to a corresponding lecture section in this course",msg_prefix="error message was printed to the user")
        updated_section = Section.objects.get(pk=self.lecture2.pk)
        self.assertIn(self.teacherassistant2,updated_section.assigned_users.all(),"user should have been assigned")

    def test_instructorCompleteValidAssignUser(self):
        resp = self.green.post("/login/",{"username":self.instructor.username,"password":self.instructor.password},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_course)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        resp = self.green.post(self.detail_url_course, {self.lecture2.pk:self.teacherassistant.pk},follow=True)
        self.assertContains(resp, "Successfully assigned user(s) to section(s)",
                            msg_prefix="message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lecture2.pk)
        self.assertIn(self.teacherassistant,updated_section.assigned_users.all(),"user should have been assigned")
        resp = self.green.post(self.detail_url_course, {self.lab1.pk:self.teacherassistant.pk},follow=True)
        self.assertContains(resp,"Successfully assigned user(s) to section(s)",msg_prefix="message was not printed to the user")
        updated_section = Section.objects.get(pk=self.lab1.pk)
        self.assertIn(self.teacherassistant,updated_section.assigned_users.all(),"user should have been assigned")



