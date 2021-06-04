from django.db import models

DEPARTMENT_CHOICES = [
    ("COMPS", "Computer"),
    ("IT", "Information Technology"),
    ("EXTC", "Electronics & Telecommunication"),
    ("MECH", "Mechanical"),
    ("BIO", "Biomedical"),
    ("ELEX", "Electronics"),
    ("CHEM", "Chemical"),
]

class Batch(models.Model):
    starting_year = models.CharField(max_length=4 , primary_key=True)
    ending_year = models.CharField(max_length=4)

class Branch(models.Model):
    b_id = models.CharField(max_length=7 , primary_key=True)
    name = models.CharField(max_length=5 , choices=DEPARTMENT_CHOICES)
    batch = models.ForeignKey(Batch , on_delete=models.CASCADE)

class Semester(models.Model):
    semester_number = models.CharField(max_length=4)
    branch = models.ForeignKey(Branch , on_delete=models.CASCADE)

class Subject(models.Model):
    subject_id = models.CharField(max_length=10 , primary_key=True)
    subject_name = models.CharField(max_length=200)
    semester = models.ForeignKey(Semester , on_delete=models.CASCADE)

class Lecture(models.Model):
    lecture_no = models.CharField(max_length=4)
    duration = models.CharField(max_length=4)
    date = models.DateField()
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    topic = models.CharField(max_length=150,null=True,blank=True)
    subject = models.ForeignKey(Subject , on_delete=models.CASCADE)

class Student(models.Model):
    sap_id = models.CharField(max_length=11,primary_key=True)
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch , on_delete=models.CASCADE)

class Attendance(models.Model):
    student = models.ForeignKey(Student , on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture , on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)