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
    day = models.CharField(max_length=9, choices=DAY_CHOICES)

    def __str__(self):
        return self.get_day_display()


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
    description = models.TextField(null=True, blank=True)
    # semester = models.CharField(max_length=6, choices=Semester.choices, default=Semester.FALL)
    semester = models.CharField(max_length=6, choices=Semesters.choices, default=Semesters.FALL)
    def __str__(self):
        return f"{self.course_id} {self.course_name} - {self.semester}"



class Section(models.Model):
    course_parent = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_id = models.IntegerField(null=True)
    type = models.CharField(max_length=7, choices=Types.choices, default=Types.LEC)
    meeting_days = models.ManyToManyField(Day, blank=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    location = models.CharField(max_length=500, null=True)
    is_online = models.BooleanField(default=False, help_text="Check if the class is online ")

    def __str__(self):
        if self.is_online:
            return f"{self.course_parent.course_name} {self.type} {self.section_id} - Online"
        else:
            days = ', '.join(day.day for day in self.meeting_days.all())
            return (f"{self.course_parent.course_name} {self.type} {self.section_id} - Days: {days}, "
                    f"Time: {self.start_time.strftime('%H:%M')} to {self.end_time.strftime('%H:%M')}, "
                    f"Location: {self.location}")


class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    role = models.CharField(max_length=17, choices=Roles.choices, default=Roles.TA)
    phone_number = models.CharField(max_length=100)
    address = models.CharField(max_length=256)
    assigned = models.BooleanField(null=True)
    assigned_section = models.ManyToManyField(Section, blank=True)
    skills = models.CharField(max_length=500, null=True)

    def __str__(self):
        return f"{self.name} {self.role}"
