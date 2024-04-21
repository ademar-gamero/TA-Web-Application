
from django.test import TestCase, Client
from django.urls import reverse
from .models import Course, Section, User

class unittest(TestCase):
    pass

#acceptance tests
class courseList(TestCase):
    green=None
    courseList=None
    def setUp(self):
        self.green = Client()
        self.courselist = {351: ["compsci", "this course covers algos and data structs"],
                      361: ["compsci", "this course covers software engineering"],
                      102: ["psych", "this course covers psychology"]}
        v=1
        z=2
        User(user_id=v,name="admin",username="admin",password="admin",email="admin@email.com",role="Admin",phone_number=1,address="1",assigned=False).save()
        User(user_id=z,name="instructor",username="instructor",password="instructor",email="instructor@email.com",role="Instructor",phone_number=1,address="1",assigned=False).save()
        self.Ausername = "admin"
        self.Apassword = "admin"
        self.Iusername = "instructor"
        self.Ipassword = "instructor"
        for i in self.courselist.keys():
            y = 0
            name = "nothing"
            descrip = "nothing"
            for x in self.courselist[i]:
                if(y == 0):
                    name = x
                if(y == 1):
                    descrip = x
                y = y + 1
            Course(course_id=i,course_name=name,description=descrip).save()

    def test_roleValidationCorrect(self):
        resp = self.green.post("/login/",{"username":self.Ausername,"password":self.Apassword},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(200,resp.status_code,"role validation failed")
        
    def test_roleValidationIncorrect(self):
        resp = self.green.post("/login/",{"username":self.Iusername,"password":admin},follow=True)
        self.assertEqual(resp.url, '/Home/')
        resp = self.green.get("/Home/courseList/")
        self.assertEqual(404,resp.status_code,"role validation failed")

    def test_displayCourses(self):
        resp = self.green.get("Home/courseList/")
        for j in resp.context["courselist"]:
            self.assertIn(j.course_name,self.courselist[j.course_id],"not all courses are listed")    

    def test_searchCourseName(self):
        search_course = "compsci"
        resp = self.green.post("Home/courseList/",{"course_name":search_course},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_name,search_course,"search is not working")

    def test_searchIncorrectCourse(self):
        search_course = "logic" 
        resp = self.green.post("Home/courseList/",{"course_name":search_course},follow=True)
        clist = resp.context["courselist"]
        checker = False
        if len(clist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")

    def test_searchIncorrectCourseID(self):
        search_courseid = 125
        resp = self.green.post("Home/courseList/",{"course_id":search_courseid},follow=True)
        clist = resp.context["courselist"]
        checker = False
        if len(clist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")

    def test_searchCourseID(self):
        search_courseid = 351
        resp = self.green.post("Home/courseList/",{"course_id":search_courseid},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_id,search_courseid,"search shouldve found a course id but didnt")

    def test_searchCourseBoth(self):
        search_courseid = 351
        search_course = "compsci"
        resp = self.green.post("Home/courseList/",{"course_id":search_courseid,"course_name":search_course},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_name,search_course,"search did not work")

    def test_searchCourseBothIncorrect(self):
        search_courseid = 123
        search_course = "sci"
        resp = self.green.post("Home/courseList/",{"course_id":search_courseid,"course_name":search_course},follow=True)
        clist = resp.context["courselist"]
        checker = False
        if len(clist) == 0:
            checker = True
        self.assertTrue(checker,"search returned a value with it shouldnt have")
    
    def test_searchCourseBothReversed(self):
        search_courseid = 351
        search_course = "compsci"
        resp = self.green.post("Home/courseList/",{"course_id":search_courseid,"course_name":search_course},follow=True)
        for j in resp.context["courselist"]:
            self.assertEqual(j.course_name,search_course,"search did not work")

