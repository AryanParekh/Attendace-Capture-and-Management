from django.urls import path
from att_man.views import *

urlpatterns = [
    path('', redirect_page , name='home'),
    path('adminlogin/',adminlogin,name='adminlogin'),
    path('capture_students/<int:lec_id>/',capture_students,name="capture_students"),
    path('student_create/',student_create,name="student_create"),
    path('manage_batchlist/',manage_batchlist,name="manage_batchlist"),
    path('manage_subjectlist/<int:semester>/',manage_subjectlist,name="manage_subjectlist"),
    path('manage_lecturelist/<str:subject>/',manage_lecturelist,name="manage_lecturelist"),
    path('manage_branchlist/<int:batch>/',manage_branchlist,name="manage_branchlist"),
    path('manage_semesterlist/<int:branch>/',manage_semesterlist,name="manage_semesterlist"),
    path('manage_studentlist/<int:lec_id>/',manage_studentlist,name="manage_studentlist"),

    path('capture_batchlist/',capture_batchlist,name="capture_batchlist"),
    path('capture_subjectlist/<int:semester>/',capture_subjectlist,name="capture_subjectlist"),
    path('capture_lecturelist/<str:subject>/',capture_lecturelist,name="capture_lecturelist"),
    path('capture_semesterlist/<int:branch>/',capture_semesterlist,name="capture_semesterlist"),
    path('capture_branchlist/<int:batch>/',capture_branchlist,name="capture_branchlist"),

]