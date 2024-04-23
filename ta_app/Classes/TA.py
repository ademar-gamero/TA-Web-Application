from . import ClassUser
from django.core.validators import EmailValidator

class TA(ClassUser):

    def edit_contact_info(self,new_contact_info):
        pass       

    def view_contact_info(self):
        pass

    def valid_email(self,email):
        pass
