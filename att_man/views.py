from django.shortcuts import render
from .models import *
from datetime import datetime

def adminlogin(request):
    if request.method=="GET":
        return render(request,'adminlogin.html')
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('redirect_page')
            else:
                return render(request,'adminlogin.html',{"error":"User is not a superuser"})
        else:
            return render(request,'adminlogin.html',{"error":"User does not exist"})

def redirect_page(request):
    # choice between management part and capture part
    pass

def manage_batchlist(request):
    if request.method == "GET":
        batches = Batch.objects.all().order_by("-starting_year")
        return render(request,'manage_batchlist.html',{"batches":batches})
    if request.method == "POST":
        starting_year = request.POST["sno"]
        graduation_year = request.POST["gno"]
        Batch.objects.create(starting_year=starting_year,ending_year=graduation_year)
        batches = Batch.objects.all().order_by("-starting_year")
        return render(request,'manage_batchlist.html',{"batches":batches})

def manage_branchlist(request, batch):
    # GET and POST request
    pass

def manage_semesterlist(request, branch):
    # GET request
    pass

def manage_subjectlist(request, semester):
    if request.method=="GET":
        subjects = Subject.objects.filter(semester=semester).order_by("subject_id")
        return render(request,'manage_subjectlist.html',{"subjects":subjects})
    if request.method=="POST":
        subject_id = request.POST["subid"]
        subject_name = request.POST["subno"]
        semester = Semester.objects.get(id=semester)
        Subject.objects.create(subject_id=subject_id,subject_name=subject_name,semester=semester)
        subjects = Subject.objects.filter(semester=semester).order_by("subject_id")
        return render(request,'manage_subjectlist.html',{"subjects":subjects})

def manage_lecturelist(request, subject):
    if request.method=="GET":
        lectures = Lecture.objects.filter(subject=subject)
        return render(request,'manage_lecturelist.html',{"lectures":lectures})
    if request.method=="POST":
        lecture_no = request.POST["lecno"]
        teacher_name = request.POST["tno"]
        date = request.POST["dno"]
        starting_time = request.POST["Stime"]
        ending_time = request.POST["Etime"]
        topic = request.POST["topic"]
        subject = Subject.objects.get(subject_id=subject)
        Lecture.objects.create(lecture_no=lecture_no,teacher_name=teacher_name,date=date,starting_time=starting_time,ending_time=ending_time,topic=topic,subject=subject)
        lectures = Lecture.objects.filter(subject=subject)
        return render(request,'manage_lecturelist.html',{"lectures":lectures})

def manage_studentlist(request):
    # GET request
    pass



def capture_batchlist(request):
    if request.method == "GET":
        batches = Batch.objects.all().order_by("-starting_year")
        return render(request,'capture_batchlist.html',{"batches":batches})

def capture_branchlist(request):
    # GET request
    pass

def capture_semesterlist(request):
    # GET request
    pass

def capture_subjectlist(request,semester):
    if request.method=="GET":
        subjects = Subject.objects.filter(semester=semester).order_by("subject_id")
        return render(request,'capture_subjectlist.html',{"subjects":subjects})

def capture_lecturelist(request,subject):
    if request.method=="GET":
        lectures = Lecture.objects.filter(subject=subject)
        return render(request,'capture_lecturelist.html',{"lectures":lectures})




