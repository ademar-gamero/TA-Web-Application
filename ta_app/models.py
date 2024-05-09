from django.db import models


class Roles(models.TextChoices):
    AD = "Admin"
    TA = "Teacher-Assistant"
    IN = "Instructor"




class Semesters(models.TextChoices):
    FALL = "Fall"
    WINT = "Winter"
    SPRI = "Spring"
    SUMM = "Summer"


class Types(models.TextChoices):
    LAB = "lab"
    LEC = "lecture"


class Course(models.Model):
    course_id = models.IntegerField(null=True)
    course_name = models.CharField(max_length=50)
    description = models.TextField(null=True,blank=True)
    semester = models.CharField(max_length=6, choices=Semesters.choices, default=Semesters.FALL)
    
    semester = models.CharField(max_length=6, choices=Semesters.choices, default=Semesters.FALL)

    def __str__(self):
        return f"{self.course_id} {self.course_name} - {self.semester}"

class Day(models.Model):
    DAY_CHOICES = [
        ('Mo', 'Monday'),
        ('Tu', 'Tuesday'),
        ('We', 'Wednesday'),
        ('Th', 'Thursday'),
        ('Fr', 'Friday'),
    ]
    day = models.CharField(max_length=9, choices=DAY_CHOICES)

    def __str__(self):
        return self.get_day_display()

class Section(models.Model):
    course_parent = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_id = models.IntegerField(null=True)
    type = models.CharField(max_length=7, choices=Types.choices, default=Types.LEC)
    meeting_days = models.ManyToManyField(Day, blank=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.course_parent.course_name} {self.type} {self.section_id}"


class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=17, choices=Roles.choices, default=Roles.TA)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=256)
    assigned = models.BooleanField(null=True)
    assigned_section = models.ManyToManyField(Section,related_name="assigned_users", blank=True)
    skills = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.name} {self.role}"
