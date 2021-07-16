from django.shortcuts import render,redirect
from .models import *
from Patients.models import *
from Reception.models import *
from django.core.mail import send_mail
from django.conf import settings
from random import *

# <----------------------------- Log In/Sign Up/Log out Start ----------------------------->
def DoctorSignUp(request):
    return render(request,"Doctor/doctor-register.html")

def DoctorLogInPage(request):
    return render(request,"Doctor/doctor-login.html")

def DoctorIndex(request):
    if 'doctorid' in request.session and 'doctoremail' in request.session:
        doctor=Doctor.objects.get(id=request.session['doctorid'])
        a=Appointments.objects.filter(DoctorId_id=doctor.id)
        p=0
        b=[]
        for i in a:
            c=i.PatientId.id
            if c not in b:
                p+=1
            b.append(c)
        a=a.count()
        d={'doctordata':doctor,'a':a,'p':p}
        return render(request,"Doctor/doctor-index.html",d)
    else:
        return render(request, "Reception/common-page.html")

def DoctorRegisterUser(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        dob=request.POST['dob']
        gender=request.POST['gender']
        address=request.POST['address']
        phone=request.POST['phone']
        department=request.POST['department']
        email=request.POST['email']
        pswd=request.POST['pswd']
        pic=request.FILES['propic']

        doctoremail=Doctor.objects.filter(Email=email)
        if len(doctoremail)>0:
            err="User Already Exist"
            return render(request,"Doctor/doctor-register.html",{'msg':err})
        else:
            if 'id' in request.session and 'emailid' in request.session:
                user=User.objects.create(FName=fname,LName=lname,Address=address,Password=pswd,Email=email,Role="Doctor")
                doctor=Doctor.objects.create(user=user,Fname=fname,Lname=lname,BirthDay=dob,Address=address,Gender=gender,Department=department,Phone_Number=phone,Email=email,Password=pswd,DStatus='Approve')
                return redirect("alldoctors")
            else:
                user=User.objects.create(FName=fname,LName=lname,Address=address,Password=pswd,Email=email,Role="Doctor")
                doctor=Doctor.objects.create(user=user,Fname=fname,Lname=lname,BirthDay=dob,Address=address,Gender=gender,Department=department,Phone_Number=phone,Email=email,Password=pswd,ProfilePic=pic)
                return redirect("Doclogin")

def DoctorLogInUser(request):
    if request.method == 'POST':
        email=request.POST['email']
        pswd=request.POST['pswd']
        doctor=Doctor.objects.filter(Email=email)
        if len(doctor)>0 and doctor[0].Role=='Doctor':
            if doctor[0].Password == pswd:
                name=Doctor.objects.get(Fname=doctor[0].Fname)
                request.session['doctorid']=doctor[0].id
                request.session['doctoremail']=doctor[0].Email
                request.session['uid']=doctor[0].user_id
                request.session['doctorfname']=name.Fname
                doctor=Doctor.objects.get(id=request.session['doctorid'])
                return redirect("Docindex") 
            else:
                err="Incorrect Password"
                return render(request,"Doctor/doctor-login.html",{'msg':err}) 
        else:
            err="User Doesn't Exist!"
            return render(request,"Doctor/doctor-login.html",{'msg':err})
    
def DoctorLogOutUser(request):
    del request.session['doctorid']
    del request.session['doctoremail']
    del request.session['doctorfname']
    return redirect("Doclogin")

# <----------------------------- Log In/Sign Up/Log out End ----------------------------->
# <----------------------------- Doctor Profile/Update Start ----------------------------->
def DoctorProfile(request):
    if 'doctorid' in request.session and 'doctoremail' in request.session:
        doctor=Doctor.objects.get(id=request.session['doctorid'])
        return render(request,"Doctor/Doctor-Profile.html",{"doctordata":doctor})

def DoctorUpdate(request):
    if request.method=='POST':
        did=Doctor.objects.get(id=request.session['doctorid'])
        usid=User.objects.get(id=request.session['uid'])
        print(f"-----USID-->{usid}")     
        did.Fname=request.POST['fname'] if request.POST['fname'] else did.Fname
        did.Lname=request.POST['lname'] if request.POST['lname'] else did.Lname
        did.BirthDay=request.POST['dob'] if request.POST['dob'] else did.BirthDay
        did.Address=request.POST['address'] if request.POST['address'] else did.Address
        did.Phone_Number=request.POST['phone'] if request.POST['phone'] else did.Phone_Number
        did.Email=request.POST['email'] if request.POST['email'] else did.Email
        did.save()

        usid.FName=request.POST['fname'] if request.POST['fname'] else usid.FName
        usid.LName=request.POST['lname'] if request.POST['lname'] else usid.LName
        usid.Email=request.POST['email'] if request.POST['email'] else usid.Email
        usid.Address=request.POST['address'] if request.POST['address'] else usid.Address
        usid.save()
        return redirect("Docprofile")
    return redirect("Docprofile")

# <----------------------------- Doctor Profile/Update End ----------------------------->
# <----------------------------- Your Patient/Appointment Start ----------------------------->
def DoctorAppointment(request):
    if 'doctorid' in request.session and 'doctoremail' in request.session:
            did=Doctor.objects.get(id=request.session['doctorid'])
            appointdetails=Appointments.objects.filter(DoctorId_id=did.id)

            return render(request,"Doctor/Doctor-Appointment.html",{"appointmentdata":appointdetails})

def DoctorPatients(request):
    if 'doctorid' in request.session and 'doctoremail' in request.session:
        did=Doctor.objects.get(id=request.session['doctorid'])
        appointdetails=Appointments.objects.filter(DoctorId_id=did.id)
        return render(request,"Doctor/Doctor-Patients.html",{"appointdetails":appointdetails})


# <----------------------------- Your Patient/Appointment End ----------------------------->
