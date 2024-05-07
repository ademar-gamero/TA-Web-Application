from django.contrib import admin
from .models import Course, Section, User, Day

admin.site.register(Day)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(User)


