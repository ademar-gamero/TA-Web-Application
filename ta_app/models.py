from django.db import models


class Roles(models.TextChoices):
    AD = "Admin"
    TA = "Teacher-Assistant"
    IN = "Instructor"


class Types(models.TextChoices):
    LAB = "lab"
    LEC = "lecture"


class Course(models.Model):
    courseID = models.IntegerField
    course_name = models.CharField(max_length=50)
    description = models.TextField

    def __str__(self):
        return self.course_name


class Section(models.Model):
    course_parent = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_id = models.IntegerField
    meeting_time = models.DateTimeField
    section_type = models.CharField(max_length=7, choices=Types.choices, default=Types.LEC)

    def __str__(self):
        return f"{self.course_parent.course_name}+{self.type}+{self.section_id}"


class User(models.Model):
    user_id = models.IntegerField
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=17, choices=Roles.choices, default=Roles.TA)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=256)
    assigned = models.BooleanField
    assigned_section = models.ManyToManyField(Section)

    def __str__(self):
        return f"{self.name} + {self.role}"




