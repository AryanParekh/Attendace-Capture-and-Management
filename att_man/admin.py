from django.contrib import admin
from .models import *

admin.site.register(Batch)
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Lecture)
admin.site.register(Student)
admin.site.register(Attendance)