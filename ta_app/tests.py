from django.test import TestCase
from classes.TA import TA
from classes.ClassUser import ClassUser

class Teacher_Assitant(TestCase):
    def setUp(self):
        self.ta = TA(1,"ta","taUser","taUser","email@email.com","Teacher-Assistant","1","street",False)
    
        self.id = 1
        self.name = "ta"
        self.username = "taUser"
        self.password = "taUser"
        self.email = "email@email.com"
        self.role="Teacher_Assistant"
        self.phone_number="1"
        self.address = "street"
        self.assigned = False
        self.assigned_section = None

    def test_TAcreation(self):
        checker = True
        if(self.name != self.ta.name):
            checker = False
        if(self.id != self.ta.username):
            checker = False
        if(self.id != self.ta.password):
            checker = False
        if(self.id != self.ta.email):
            checker = False
        if(self.id != self.ta.role):
            checker = False
        if(self.id != self.ta.phone_number):
            checker = False
        if(self.id != self.ta.address):
            checker = False
        if(self.id != self.ta.assigned):
            checker = False
        if(self.id != self.ta.address):
            checker = False
        if(self.assigned_section != self.ta.assigned_section)
            checker = False
        self.assertEqual(checker, "invalid TA creation")

    def test_viewContactInformation(self):
        contact_info = ta.view_contact_info()
        self.assertEqual(contact_info,self.email)

    def test_editContactInformation(self):
        new_contact_info = "american@email.com" 
        ta.edit_contact_info("american@email.com")
        self.assertEqual(new_contact_info,ta.email,"contact info was not changed")

    def test_editContactInfoInteger(self):
        with self.assertRaises(TypeError, msg = "you passed in a non numberic value"):
            ta.edit_contact_info(1)

    def test_invalidEmail(self):
        self.assertFalse(ta.valid_email("americanemail.com"),"email validation failed")

    def test_validEmail(self):
        self.assertTrue(ta.valid_email("american@email.com"),"email validation failed")

    def test_editContactInfoInvalidCheck(self):
        ta.edit_contact_info("americanemail.com")
        self.assertEqual(self.ta.email,"email@email.com","email validation failed")

