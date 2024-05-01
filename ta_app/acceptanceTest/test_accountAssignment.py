
from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User
from datetime import time


class accountAssignment(TestCase):
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
        self.sec = Section.objects.create(course_parent = self.algos,section_id=1,type="lecture",location="classroom")
        self.sec.save()
        self.sec2 = Section.objects.create(course_parent = self.algos,section_id=2,type="lecture",location="classroom")
        self.sec.save()
        self.accountList = [self.admin,self.instructor]
        self.detail_url_ins = reverse('accountAssignment',args=[self.instructor.pk])
        self.detail_url_ta = reverse('accountAssignment',args=[self.teacherassistant.pk])
        self.instructor2.assigned_section.add(self.sec)
        self.instructor2.save()
        self.lecture2 = Section.objects.create(parent=self.course1, section_id=101, type="LEC",
                                               start_time=time(12, 0), end_time=time(1, 30),
                                               meeting_day=["TU", "TH"],location="class25b")
        self.lecture3 = Section.objects.create(parent=self.course1, section_id=102, type="LEC",
                                               start_time=time(11, 0), end_time=time(12, 30),
                                               meeting_day=["MO", "WE"],location="class30B")

    def test_validAccessAccAssignment(self):
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

    def test_removeAssignment(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.get("/Home/accountList/accountAssignment/Delete/1/")
        self.assertEqual(200,resp.status_code,"delete page was not displayed")

    def test_addAssignmentInstructor(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url,{"section":self.sec})
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertIn(self.sec,new.assigned_section, "sections was not added")

    def test_addMultipleAssignmentInstructor(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url,{"section":self.sec})
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        resp = self.green.post(self.detail_url,{"section":self.sec2})
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertIn(self.sec,new.assigned_section, "sections was not added")
        self.assertIn(self.sec2,new.assigned_section, "sections was not added")

    def test_addMultipleAssignmentInstructor(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)

        resp = self.green.get("/Home/accountList/")
        self.assertEqual(200,resp.status_code,"role error")
        resp = self.green.get(self.detail_url)
        self.assertEqual(200,resp.status_code,"page was not displayed")

        resp = self.green.post(self.detail_url,{"section":self.section2})
        self.assertTrue(resp.context['message'], "Section was successfully added!")
        resp = self.green.post(self.detail_url,{"section":self.section3})
        self.assertTrue(resp.context['message'], "Section was not added a time conflict exists")
        new = User.objects.get(pk=self.instructor.pk)
        self.assertIn(self.section2,new.assigned_section, "sections was not added")
        self.assertNotIn(self.section3,new.assigned_section, "sections was added when it shouldnt have been")

