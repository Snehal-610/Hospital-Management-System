from django.shortcuts import render,redirect
from .models import *
from Reception.models import *
from Doctor.models import *
# Create your views here.
# ----------------------- Basic Patient Section -----------------------
def PatientSignUp(request):
    doc = Doctor.objects.all().values()
    return render(request,"Patients/Patient-register.html",{'doctordata':doc})

def PatientLogInPage(request):
    return render(request,"Patients/Patient-login.html")

def PatientIndex(request):
    if 'Patientid' in request.session and 'Patientemail' in request.session:
        patient=Patients.objects.get(id=request.session['Patientid'])
        doctor=Doctor.objects.get(id=patient.DoctorId_id)
        p={"patientdata":patient,"doctor":doctor}
        return render(request,"Patients/Patient-index.html",p)
    else:
        return render(request, "Reception/common-page.html")

# ----------------------- Registration / Log In / LogOut Start -----------------------
def PatientRegisterUser(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        gender=request.POST['gender']
        adress=request.POST['address']
        phone=request.POST['phone']
        age=int(request.POST['age'])
        symptoms=request.POST['symptoms']
        email=request.POST['email']
        pswd=request.POST['pswd']
        docinformation=request.POST['docter']
        
        doctorid=docinformation.split()
        did=Doctor.objects.get(id=doctorid[0])
        
        Patientemail=Patients.objects.filter(Email=email)
        if len(Patientemail)>0:
            err="Patient Already Exist"
            doc = Doctor.objects.all().values()
            return render(request,"Patients/Patient-register.html",{'msg':err,'data':doc})
        else:
            if 'id' in request.session and 'emailid' in request.session:
                user=User.objects.create(FName=fname,LName=lname,Address=adress,Password=pswd,Email=email,Role="Patient") 
                patient=Patients.objects.create(user=user,DoctorId=did,Fname=fname,Lname=lname,Address=adress,Gender=gender,Symptoms=symptoms,Phone_Number=phone,Email=email,Password=pswd,Age=age,status="Approve")
            else:
                user=User.objects.create(FName=fname,LName=lname,Address=adress,Password=pswd,Email=email,Role="Patient") 
                patient=Patients.objects.create(user=user,DoctorId=did,Fname=fname,Lname=lname,Address=adress,Gender=gender,Symptoms=symptoms,Phone_Number=phone,Email=email,Password=pswd,Age=age)
    return redirect("Patientlogin")

def PatientLogInUser(request):
    if request.method == 'POST':
        email=request.POST['email']
        pswd=request.POST['pswd']
        patient=Patients.objects.filter(Email=email)
        if len(patient)>0 and patient[0].Role=='Patient':
            if patient[0].Password == pswd:
                name=Patients.objects.get(Fname=patient[0].Fname)
                request.session['Patientid']=patient[0].id
                request.session['Patientemail']=patient[0].Email
                request.session['uid']=patient[0].user_id
                request.session['Patientfname']=name.Fname
                patient=Patients.objects.get(id=request.session['Patientid'])
                return redirect("Patientindex")      
            else:
                err="Incorrect Password"
                return render(request,"Patients/Patient-login.html",{'msg':err}) 
        else:
            err="Patient Doesn't Exist!"
            return render(request,"Patients/Patient-login.html",{'msg':err})
    
def PatientLogOutUser(request):
    del request.session['Patientid']
    del request.session['Patientemail']
    del request.session['Patientfname']
    return redirect("Patientlogin")

# ----------------------- Registration / Log In / LogOut End -----------------------
# ----------------------- Patient Profile/Update Start -----------------------
def PatientProfile(request):
    if 'Patientid' in request.session and 'Patientemail' in request.session:
        patient=Patients.objects.get(id=request.session['Patientid'])
        doctor=Doctor.objects.get(id=patient.DoctorId_id)
        p={"patientdata":patient,"doctor":doctor}
        return render(request,"Patients/Patient-Profile.html",p)

def PatientUpdate(request):
    if request.method=='POST':
        did=Patients.objects.get(id=request.session['Patientid'])
        did.Fname=request.POST['fname'] if request.POST['fname'] else did.Fname
        did.Lname=request.POST['lname'] if request.POST['lname'] else did.Lname
        did.Gender=request.POST['gender'] if request.POST['gender'] else did.Gender
        did.Email=request.POST['email'] if request.POST['email'] else did.Email
        did.Phone_Number=request.POST['phone'] if request.POST['phone'] else did.Phone_Number
        did.Symptoms=request.POST['symptoms'] if request.POST['symptoms'] else did.Symptoms
        did.Address=request.POST['address'] if request.POST['address'] else did.Address
        did.save()

        usid=User.objects.get(id=request.session['uid'])   
        usid.FName=request.POST['fname'] if request.POST['fname'] else usid.FName
        usid.LName=request.POST['lname'] if request.POST['lname'] else usid.LName
        usid.Email=request.POST['email'] if request.POST['email'] else usid.Email
        usid.Address=request.POST['address'] if request.POST['address'] else usid.Address
        usid.save()
    return redirect("patientprofile")

# ----------------------- Patient Profile/Update End -----------------------
# ----------------------- AppointMent Section Start -----------------------
def BookAppointment(request):
    if 'Patientid' in request.session and 'Patientemail' in request.session: 
        patient=Patients.objects.get(id=request.session['Patientid'])
        doctor=Doctor.objects.all().values()
        p={"patientdata":patient,"docdata":doctor}
        return render(request,"Reception/book-appointment.html",p)
    else:
        return render(request,"Patients/Patient-login.html")

def RequestAppointment(request):
    if 'Patientid' in request.session and 'Patientemail' in request.session:
        if request.method=='POST':
            pid=Patients.objects.get(id=request.session['Patientid'])
            docinformation=request.POST['docinfo']
            discription=request.POST['discription']
            appointmentdate=request.POST['appointmentdate']
            doctorid=docinformation.split()
            did=Doctor.objects.get(id=doctorid[0])
            appointment=Appointments.objects.create(PatientId=pid,DoctorId=did,AppointmentDate=appointmentdate,Discription=discription)
            p={'patientdata':pid,'doctordata':did,"appointmentdata":appointment}
            return render(request,"Patients/Patient-Appointment.html",p)
    else:
        return redirect("Patientlogin")

def PatientAppointment(request):
    if 'Patientid' in request.session and 'Patientemail' in request.session:
            pid=Patients.objects.get(id=request.session['Patientid'])
            appointdetails=Appointments.objects.filter(PatientId_id=pid.id)
            p={'patientdata':pid,"appointmentdata":appointdetails}
            return render(request,"Patients/Patient-Appointment.html",p)

# ----------------------- AppointMent Section End -----------------------
