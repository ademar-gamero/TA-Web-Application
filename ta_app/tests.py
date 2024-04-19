from django.test import TestCase
from ta_app.classes.TA import TA
from ta_app.classes.UserClass import UserClass

class Teacher_Assitant(TestCase):
    def setUp(self):
        self.ta = TA("taUser","taUser","ta","Teacher-Assistant","email@email.com","1","street",False)
    
        self.name = "ta"
        self.username = "taUser"
        self.password = "taUser"
        self.email = "email@email.com"
        self.role="Teacher-Assistant"
        self.phone_number="1"
        self.address = "street"
        self.assigned = False
        self.assigned_section = []

    def test_TAcreation(self):
        self.assertEqual(self.name,self.ta.name,"error: ta name field is incorrect")
        self.assertEqual(self.username,self.ta.username,"error: ta name field is incorrect")
        self.assertEqual(self.password,self.ta.password,"error: ta name field is incorrect")
        self.assertEqual(self.email,self.ta.email,"error: ta name field is incorrect")
        self.assertEqual(self.role,self.ta.role,"error: ta name field is incorrect")
        self.assertEqual(self.phone_number,self.ta.phone_number,"error: ta name field is incorrect")
        self.assertEqual(self.address,self.ta.address,"error: ta name field is incorrect")
        self.assertEqual(self.assigned,self.ta.assigned,"error: ta name field is incorrect")
        self.assertEqual(self.assigned_section,self.ta.assigned_sections,"error: ta name field is incorrect")

    def test_viewContactInformation(self):
        contact_info = self.ta.view_contact_info()
        self.assertEqual(contact_info,self.email)

    def test_editContactInformation(self):
        new_contact_info = "american@email.com" 
        self.ta.edit_contact_info("american@email.com")
        self.assertEqual(new_contact_info,self.ta.email,"contact info was not changed")

    def test_editContactInfoInteger(self):
        with self.assertRaises(TypeError, msg = "you passed in a non numberic value"):
            self.ta.edit_contact_info(1)

    def test_invalidEmail(self):
        self.assertFalse(self.ta.valid_email("americanemail.com"),"email validation failed")

    def test_validEmail(self):
        self.assertTrue(self.ta.valid_email("american@email.com"),"email validation failed")

    def test_editContactInfoInvalidCheck(self):
        self.ta.edit_contact_info("americanemail.com")
        self.assertEqual(self.ta.email,"email@email.com","email validation failed")

