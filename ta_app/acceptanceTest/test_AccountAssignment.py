
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
        self.instructor2 = User.objects.create(name="bob", username="bob", password="instructor",
                                               email="inst@email.com", role="Instructor", phone_number=3, address="1",
                                               assigned=False)
        self.algos = Course(course_id=351, course_name="compsci", description="blah blah blah", semester="Summer")
        self.algos.save()

        self.lecture1 = Section.objects.create(course_parent=self.algos, section_id=101, type="lecture",
                                               start_time=time(12, 0), end_time=time(1, 30), location="class25b")

        self.lecture1.meeting_days.add(self.monday, self.wednesday)
        self.lecture1.save()

        self.lecture2 = Section.objects.create(course_parent=self.algos, section_id=102, type="lecture",
                                               start_time=time(12, 0), end_time=time(1, 30), location="class26b")

        self.lecture2.meeting_days.add(self.wednesday)
        self.lecture2.save()

        self.lecture3 = Section.objects.create(course_parent=self.algos, section_id=103, type="lecture",
                                               start_time=time(3, 0), end_time=time(7, 30), location="class27b")

        self.lecture3.meeting_days.add(self.friday)
        self.lecture3.save()

        self.lab1 = Section.objects.create(course_parent=self.algos, section_id=102, type="lab",
                                           start_time=time(11, 0), end_time=time(12, 30), location="class30B")

        self.lab1.meeting_days.add(self.thursday)
        self.lab1.save()

        self.lab2 = Section.objects.create(course_parent=self.algos, section_id=105, type="lab",
                                           start_time=time(11, 0), end_time=time(12, 30), location="class45C")

        self.lab2.meeting_days.add(self.tuesday, self.thursday)
        self.lab2.save()

        self.detail_url_course = reverse('courseSections', args=[self.algos.pk])

        self.instructor2.assigned_section.add(self.lecture1)
        self.instructor2.save()

        self.teacherassistant.assigned_section.add(self.lecture1)
        self.teacherassistant.save()

        self.detail_url_ins = reverse('accountAssignment',args=[self.instructor.pk])
        self.detail_url_ins2 = reverse('accountAssignment', args=[self.instructor2.pk])
        self.detail_url_ta = reverse('accountAssignment',args=[self.teacherassistant.pk])
        self.detail_url_ta2 = reverse('accountAssignment', args=[self.teacherassistant2.pk])


    def test_validAccessAccAssignment(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        self.green.get(self.detail_url_ta)
        self.assertEqual(200,resp.status_code,"page was not displayed")

    def test_validInstructorAccessEditAcc(self):
        resp = self.green.post("/login/",{"username":self.instructor.username,"password":self.instructor.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"account list web page not setup properly")
        resp = self.green.get(self.detail_url_ta)
        self.assertEqual(200,resp.status_code,"role validation failed")


    def test_validTeacherAssistantAccessEditAcc(self):
        resp = self.green.post("/login/",{"username":self.teacherassistant.username,"password":self.teacherassistant.password},follow=True)
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"account list web page not setup properly")
        resp = self.green.get(self.detail_url_ins)
        self.assertEqual(200,resp.status_code,"role validation failed")


    def test_removeAssignment(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ta2)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"Remove Assignment",msg_prefix="Remove Assignement was not displayed")

    def test_courseAssignments(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ins2)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertContains(resp,"351 compsci",msg_prefix="compsci was not displayed")


    def test_instructorRemoveAssignment(self):
        resp = self.green.post("/login/",{"username":self.instructor.username,"password":self.instructor.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ta2)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertContains(resp,"Remove Assignment",msg_prefix="Remove Assignement was not displayed")


    def test_taRemoveAssignment(self):
        resp = self.green.post("/login/",{"username":self.instructor.username,"password":self.instructor.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ta2)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"Remove Assignment",msg_prefix="Remove Assignement was displayed when it shouldnt have been")

    def test_taAddAssignment(self):
        resp = self.green.post("/login/",{"username":self.instructor.username,"password":self.instructor.password},follow=True)
        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ta2)
        self.assertEqual(200,resp.status_code,"page was not displayed")
        self.assertNotContains(resp,"Add Section:",msg_prefix="Add Section was displayed when it shouldnt have been")


    def test_adminAddAssignmentInstructor(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ins)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url_ins,{"section":self.lecture1})
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertIn(self.lecture1,new.assigned_section, "sections was not added")
        self.assertTrue(new.assigned,"assigned did not properly change")

    def test_instructorAddAssignmentTa(self):
        resp = self.green.post("/login/", {"username": self.instructor.username, "password": self.instructor.password}, follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200, resp.status_code, "role error")
        resp = self.green.get(self.detail_url_ta2)
        self.assertEqual(200, resp.status_code, "page was not displayed")

        resp = self.green.post(self.detail_url_ta2, {"section": self.lab1})
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        new = User.objects.get(pk=self.teacherassistant2.pk)
        self.assertIn(self.lecture1, new.assigned_section, "sections was not added")
        self.assertTrue(new.assigned,"assigned did not properly change")

    def test_addMultipleAssignmentInstructor(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ins)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url_ins,{"section":self.lecture2.pk},follow=True)
        new1 = User.objects.get(pk=self.instructor.pk)
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        self.assertIn(self.lecture2,new1.assigned_section.all(), "sections was not added")

        resp = self.green.post(self.detail_url_ins,{"section":self.lecture3.pk},follow=True)
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        new2 = User.objects.get(pk=self.instructor.pk)
        self.assertIn(self.lecture3,new2.assigned_section.all(), "sections was not added")

    def test_addMultipleInvalidAssignmentInstructor(self):
        resp = self.green.post("/login/",{"username":self.admin.username,"password":self.admin.password},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url_ins)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url_ins,{"section":self.lecture1},follow=True)
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        resp = self.green.post(self.detail_url_ins,{"section":self.lecture2},follow=True)
        self.assertTrue(resp.context['message'], "Section was not added a time conflict exists")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertIn(self.lecture1,new.assigned_section, "sections was not added")
        self.assertNotIn(self.lecture2,new.assigned_section, "sections was added when it shouldnt have been")

