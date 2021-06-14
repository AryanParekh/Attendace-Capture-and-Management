from django.urls import path
from att_man.views import *

urlpatterns = [
    # path('',  , name='home'),
    path('manage_batchlist/',manage_batchlist,name="manage_batchlist"),
    path('manage_subjectlist/<int:semester>/',manage_subjectlist,name="manage_subjectlist"),
    path('manage_lecturelist/<str:subject>/',manage_lecturelist,name="manage_lecturelist"),

    path('capture_batchlist/',capture_batchlist,name="capture_batchlist"),
    path('capture_subjectlist/<int:semester>/',capture_subjectlist,name="capture_subjectlist"),
    path('capture_lecturelist/<str:subject>/',capture_lecturelist,name="capture_lecturelist"),
]