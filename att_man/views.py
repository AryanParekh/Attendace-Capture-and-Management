from django.shortcuts import redirect, render
from .models import *
from datetime import datetime
from django.http import HttpResponseRedirect
import cv2
import face_recognition
import numpy as np
from django.contrib.auth import authenticate,login

BRANCH = [
    "COMPS",
    "IT", 
    "EXTC",
    "MECH",
    "BIO",
    "ELEX",
    "CHEM",
]

def student_create(request):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method=="GET":
        batches = Batch.objects.all()
        return render(request,'student_create2.html',{'branch':BRANCH,'batch':batches})
    if request.method=="POST":
        batches = Batch.objects.all()
        sap_id=request.POST["sap_id"]
        name=request.POST["name"]
        branch=request.POST["branch"]
        batch=request.POST["batch"].split("-")[0][0:-1]
        batch = Batch.objects.get(starting_year=batch)
        pic=request.FILES.get("photo")
        branch =  Branch.objects.get(name=branch,batch=batch)
        student = Student.objects.create(sap_id=sap_id,name=name,branch=branch,image=pic)
        import os
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+student.image.url
        # image = cv2.imread(r'C:\Users\aryan\Desktop\Attendance Capture and Management\Attendance_capture'+student.image.url)
        image = cv2.imread(path)
        face_encod = face_recognition.face_encodings(image)[0]
        student.description = face_encod
        student.save()
        return HttpResponseRedirect('/')
        # return render(request,'student_create2.html',{'branch':BRANCH,'batch':batches})

def adminlogin(request):
    if request.method=="GET":
        return render(request,'login.html')
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                return render(request,'login.html',{"error":"User is not a superuser"})
        else:
            return render(request,'login.html',{"error":"Please Check your username or password"})

def redirect_page(request):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    return render(request,'redirect_page2.html')

def manage_batchlist(request):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method == "GET":
        batches = Batch.objects.all().order_by("-starting_year")
        return render(request,'manage_batchlist2.html',{"batches":batches})
    if request.method == "POST":
        starting_year = request.POST["sno"]
        graduation_year = request.POST["gno"]
        Batch.objects.create(starting_year=starting_year,ending_year=graduation_year)
        batches = Batch.objects.all().order_by("-starting_year")
        return render(request,'manage_batchlist2.html',{"batches":batches})

def manage_branchlist(request, batch):  
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/') 
    if request.method == "GET":
        branches = Branch.objects.filter(batch = batch)
        batch = Batch.objects.get(starting_year=batch)
        return render(request,'manage_branchlist2.html',{'branches':branches,'batch':batch})
    if request.method == "POST":
        b_id = request.POST['gno']
        branch_name = request.POST['branch']
        batch_in = Batch.objects.get(starting_year = batch)
        branch = Branch.objects.create(b_id=b_id,name=branch_name,batch=batch_in)
        for sem in range(1,9):
            Semester.objects.create(semester_number=sem,branch=branch)
        branches = Branch.objects.filter(batch = batch)
        return render(request,'manage_branchlist2.html',{'branches':branches,'batch':batch_in})

def manage_semesterlist(request, branch):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method == "GET":
        semester = Semester.objects.filter(branch=branch)
        branch = Branch.objects.get(b_id=branch)
        return render(request,'manage_semesterlist2.html',{'semester':semester,'branch':branch})

def manage_subjectlist(request, semester):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method=="GET":
        subjects = Subject.objects.filter(semester=semester).order_by("subject_id")
        semester = Semester.objects.get(id=semester)
        return render(request,'manage_subjectlist2.html',{"subjects":subjects,"semester":semester})
    if request.method=="POST":
        subject_id = request.POST["subid"]
        subject_name = request.POST["subno"]
        semester = Semester.objects.get(id=semester)
        Subject.objects.create(subject_id=subject_id,subject_name=subject_name,semester=semester)
        subjects = Subject.objects.filter(semester=semester).order_by("subject_id")
        return render(request,'manage_subjectlist2.html',{"subjects":subjects,"semester":semester})

def manage_lecturelist(request, subject):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method=="GET":
        lectures = Lecture.objects.filter(subject=subject)
        subject = Subject.objects.get(subject_id=subject)
        return render(request,'manage_lecturelist2.html',{"lectures":lectures,"subject":subject})
    if request.method=="POST":
        lecture_no = request.POST["lecno"]
        teacher_name = request.POST["tno"]
        date = request.POST["dno"]
        starting_time = request.POST["Stime"]
        ending_time = request.POST["Etime"]
        topic = request.POST["topic"]
        subject = Subject.objects.get(subject_id=subject)
        lec = Lecture.objects.create(lecture_no=lecture_no,teacher_name=teacher_name,date=date,starting_time=starting_time,ending_time=ending_time,topic=topic,subject=subject)
        semester = Subject.objects.get(subject_id=subject.subject_id).semester
        branch = Semester.objects.get(id=semester.id).branch
        student_list = Student.objects.filter(branch=branch)
        for student in student_list:
            Attendance.objects.create(student=student,lecture=lec)
        lectures = Lecture.objects.filter(subject=subject)
        return render(request,'manage_lecturelist2.html',{"lectures":lectures,"subject":subject})

def manage_studentlist(request,lec_id):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method == "GET":
        lecture = Lecture.objects.get(id=lec_id)
        subject = lecture.subject
        semester = Subject.objects.get(subject_id=subject.subject_id).semester
        branch = Semester.objects.get(id=semester.id).branch
        students = []
        student_list = Student.objects.filter(branch=branch)
        for student in student_list:
            attendance = Attendance.objects.get(student=student,lecture__id=lec_id)
            attended = str(attendance.attended)
            students.append((student,attended,attendance.time))

        return render(request,'manage_studentlist2.html',{"students":students,'lecture':lecture})

def capture_batchlist(request):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method == "GET":
        batches = Batch.objects.all().order_by("-starting_year")
        return render(request,'capture_batchlist2.html',{"batches":batches})

def capture_branchlist(request,batch):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method == "GET":
        branches = Branch.objects.filter(batch = batch)
        batch = Batch.objects.get(starting_year=batch)
        return render(request,'capture_branchlist2.html',{'branches':branches,'batch':batch})

def capture_semesterlist(request,branch):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method == "GET":
        semester = Semester.objects.filter(branch=branch)
        branch = Branch.objects.get(b_id=branch)
        return render(request,'capture_semesterlist2.html',{'semester':semester,'branch':branch})
   
def capture_subjectlist(request,semester):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method=="GET":
        subjects = Subject.objects.filter(semester=semester).order_by("subject_id")
        semester = Semester.objects.get(id=semester)
        return render(request,'capture_subjectlist2.html',{"subjects":subjects,"semester":semester})

def capture_lecturelist(request,subject):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method=="GET":
        lectures = Lecture.objects.filter(subject=subject)
        subject = Subject.objects.get(subject_id=subject)
        return render(request,'capture_lecturelist2.html',{"lectures":lectures,"subject":subject})




def capture_attendance(encode_list,sap_ids):
    cap = cv2.VideoCapture(0) 
    marked_set = set()
    time_list = []
    while True: 
        ret, frame = cap.read(0) 
        frame_size = cv2.resize(frame,(0,0),None,0.5,0.5)
        frame_size = cv2.cvtColor(frame_size,cv2.COLOR_BGR2RGB)
        face_loc = face_recognition.face_locations(frame_size)
        encode = face_recognition.face_encodings(frame_size,face_loc)
        for encode_face,face_location in zip(encode,face_loc):
            matches = face_recognition.compare_faces(encode_list,encode_face)
            face_dis = face_recognition.face_distance(encode_list,encode_face)
            match_idx = np.argmin(face_dis)
            if matches[match_idx]:
                name = sap_ids[match_idx]
                y1,x2,y2,x1 = face_loc[0]
                y1,x2,y2,x1 = y1*2,x2*2,y2*2,x1*2
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),5)
                if name not in marked_set:
                    time_list.append((name,datetime.now()))
                    cv2.putText(frame,"Done",(x1+10,y2-10),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
                else:
                    cv2.putText(frame,"Already Done",(x1+10,y2-10),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
                marked_set.add(name)
                # break
        cv2.imshow('Video Face Detection', frame) 
        c = cv2.waitKey(10) 
        if c == 27: 
            break 
    cap.release() 
    cv2.destroyAllWindows()
    return time_list


def capture_students(request,lec_id):
    if request.user.is_superuser == False:
        return HttpResponseRedirect('/adminlogin/')
    if request.method == "GET":
        lecture = Lecture.objects.get(id=lec_id)
        subject = lecture.subject
        semester = Subject.objects.get(subject_id=subject.subject_id).semester
        branch = Semester.objects.get(id=semester.id).branch
        sap_ids = []
        encode_list = []
        student_list = Student.objects.filter(branch=branch)
        for student in student_list:
            sap_ids.append(student.sap_id)
            x = np.array(student.description.split())
            x[0] = x[0][1:]
            x[-1] = x[-1][0:-1]
            x = np.float32(x)
            encode_list.append(x)
        time_list = capture_attendance(encode_list,sap_ids)
        for sap_id,time in time_list:
            student = Student.objects.get(sap_id=sap_id)
            attendance = Attendance.objects.get(student=student,lecture=lecture)
            if attendance.attended==False:
                attendance.attended=True
                attendance.time=time
                attendance.save()
        return HttpResponseRedirect('/manage_studentlist/'+str(lec_id)+'/')




