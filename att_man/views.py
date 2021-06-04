from django.shortcuts import render

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
    # GET and POST request
    pass

def manage_branchlist(request):
    # GET and POST request
    pass

def manage_semesterlist(request):
    # GET request
    pass

def manage_subjectlist(request):
    # GET and POST request
    pass

def manage_lecturelist(request):
    # GET and POST request    
    pass

def manage_studentlist(request):
    # GET request
    pass



def capture_batchlist(request):
    # GET request
    pass

def capture_branchlist(request):
    # GET request
    pass

def capture_semesterlist(request):
    # GET request
    pass

def capture_subjectlist(request):
    # GET request
    pass

def capture_lecturelist(request):
    # GET request
    pass




