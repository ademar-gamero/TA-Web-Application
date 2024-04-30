from django.db import models

class Roles(models.TextChoices):
    AD = "Admin"
    TA = "Teacher-Assistant"
    IN = "Instructor"

class Day(models.Model):
    DAY_CHOICES = [
        ('Mo', 'Monday'),
        ('Tu', 'Tuesday'),
        ('We', 'Wednesday'),
        ('Th', 'Thursday'),
        ('Fr', 'Friday'),
    ]
    day = models.CharField(max_length=2, choices=DAY_CHOICES, unique=True)

    def __str__(self):
        return self.get_day_display()

class Types(models.TextChoices):
    LAB = "lab"
    LEC = "lecture"

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.course_id} - {self.course_name}"

class Section(models.Model):
    course_parent = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_id = models.AutoField(primary_key=True)
    meeting_days = models.ManyToManyField(Day, blank=True)
    meeting_time = models.CharField(max_length=20, blank=True, help_text="Format: HH:MM-HH:MM AM/PM")
    type = models.CharField(max_length=7, choices=Types.choices, default=Types.LEC)

    def __str__(self):
        day_names = ", ".join([day.get_day_display() for day in self.meeting_days.all()])
        return f"{self.course_parent.course_name} - {self.type} [{day_names}] at {self.meeting_time}"
class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)  # Consider using Django's User model for authentication
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=17, choices=Roles.choices, default=Roles.TA)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=256)
    assigned = models.BooleanField(default=False)
    #assigned = models.BooleanField(null=True) # shouldnt be dedaulted to false
    assigned_section = models.ManyToManyField(Section, blank=True, related_name='assigned_users')
    def __str__(self):
        return f"{self.name} ({self.role})"
