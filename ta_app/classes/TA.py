from .UserClass import UserClass
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class TA(UserClass):

    def edit_contact_info(self,new_contact_info):
        if self.valid_email(new_contact_info) == True:
            self.email = new_contact_info
            return True
        return False

    def view_contact_info(self):
        return self.email

    def valid_email(self,email):
        try:
            validate_email(email)
        except ValidationError:
           return False
        else:
           return True
