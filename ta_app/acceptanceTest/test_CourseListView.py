
from django.test import TestCase, Client
from django.urls import reverse
from ta_app.models import Course, Section, User

#acceptance tests
class courseList(TestCase):
    green=None
    courseList=None
    def setUp(self):
        self.green = Client()
        self.courselist = {351: ["compsci", "this course covers algos and data structs","Summer"],
                      361: ["compsci", "this course covers software engineering","Winter"],
                      102: ["psych", "this course covers psychology","Summer"]}
        User(name="admin",username="admin",password="admin",email="admin@email.com",role="Admin",phone_number=1,address="1",assigned=False).save()
        User(name="instructor",username="instructor",password="instructor",email="instructor@email.com",role="Instructor",phone_number=1,address="1",assigned=False).save()
        self.Ausername = "admin"
        self.Apassword = "admin"
        self.Iusername = "instructor"
        self.Ipassword = "instructor"
        for i in self.courselist.keys():
            y = 0
            semester = "nothing"
            name = "nothing"
            descrip = "nothing"
            for x in self.courselist[i]:
                if(y == 0):
                    name = x
                if(y == 1):
                    descrip = x
                if(y == 2):
                    semester = x
                y = y + 1
            Course(course_id=i,course_name=name,description=descrip,semester=semester).save()

    def test_accessAdmin(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role validation failed")
        
    def test_accessInstructor(self):
        resp = self.green.post("/login/",{"username":self.Iusername,"password":self.Ipassword},follow=True)
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role validation failed")

    def test_displayCourses(self):
        resp = self.green.get("/Home/courseList/")
        for j in resp.context["courselist"]:
            self.assertIn(j.course_name,self.courselist[j.course_id],"not all courses are listed")    

    def test_searchCourseName(self):
        search_course = "compsci"
        resp = self.green.post("/Home/courseList/",{"course_name":search_course},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_name,search_course,"search is not working")

    def test_searchIncorrectCourse(self):
        search_course = "logic" 
        resp = self.green.post("/Home/courseList/",{"course_name":search_course},follow=True)
        clist = resp.context["courselist"]
        checker = False
        if len(clist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")

    def test_searchIncorrectCourseID(self):
        search_courseid = 125
        resp = self.green.post("/Home/courseList/",{"course_id":search_courseid},follow=True)
        clist = resp.context["courselist"]
        checker = False
        if len(clist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")

    def test_searchCourseID(self):
        search_courseid = 351
        resp = self.green.post("/Home/courseList/",{"course_id":search_courseid},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_id,search_courseid,"search shouldve found a course id but didnt")

    def test_searchCourseBoth(self):
        search_courseid = 351
        search_course = "compsci"
        resp = self.green.post("/Home/courseList/",{"course_id":search_courseid,"course_name":search_course},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_name,search_course,"search did not work")

    def test_searchCourseBothIncorrect(self):
        search_courseid = 123
        search_course = "sci"
        resp = self.green.post("/Home/courseList/",{"course_id":search_courseid,"course_name":search_course},follow=True)
        clist = resp.context["courselist"]
        checker = False
        if len(clist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")
    
    def test_searchCourseBothReversed(self):
        search_courseid = 351
        search_course = "compsci"
        resp = self.green.post("/Home/courseList/",{"course_id":search_courseid,"course_name":search_course},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_name,search_course,"search did not work")

    def test_searchtriple(self):
        search_courseid = 351
        search_course = "compsci"
        search_semester = "Summer"
        resp = self.green.post("/Home/courseList/",{"course_id":search_courseid,"course_name":search_course,"semesters":search_semester},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_name,search_course,"search did not work")
        clist = resp.context['courselist']
        self.assertTrue(len(clist) == 1)

    def test_searchNothing(self):
        search_courseid = ""
        search_course = ""
        search_semester = ""
        resp = self.green.post("/Home/courseList/",{"course_id":search_courseid,"course_name":search_course,"semesters":search_semester},follow=True)
        clist = resp.context['courselist']
        self.assertTrue(len(clist) == 3)

    def test_searchSemester(self):
        search_semester = "Summer"
        resp = self.green.post("/Home/courseList/",{"semesters":search_semester},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.semester,search_semester,"search did not work")
        clist = resp.context['courselist']
        self.assertTrue(len(clist) == 2)

    def test_searchSemesterInvalid(self):
        search_semester = "Spring"
        resp = self.green.post("/Home/courseList/",{"semesters":search_semester},follow=True)
        clist = resp.context['courselist']
        self.assertTrue(len(clist) == 0)



