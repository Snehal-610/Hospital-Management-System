import Reception
from django.shortcuts import render,redirect
from .models import *
from Doctor.models import *
from Patients.models import *
from random import *
from django.core.mail import send_mail
from django.conf import settings
from datetime import date

# ----------------------- Basic Reception Section -----------------------
def IndexPage(request):
    if 'id' in request.session and 'emailid' in request.session:
        user=User.objects.get(id=request.session['id'])
        d=Doctor.objects.all().count()
        p=Patients.objects.all().count()
        a=Appointments.objects.all().count()
        d1={'data':user,'d':d,'p':p,'a':a}
        return render(request, "Reception/index.html",d1)
    else:
        return render(request, "Reception/common-page.html")

def LogInPage(request):
    return render(request, "Reception/login.html")

def RegisterPage(request):
    return render(request, "Reception/register.html")

# -----------------------  Registration / Log In / LogOut Start -----------------------
def RegisterUser(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        address=request.POST['address']
        email=request.POST['email']
        paswd=request.POST['pswd']

        check=User.objects.filter(Email=email)
        if len(check)>0:
            err="User Already Exist !"
            return render(request,"Reception/register.html",{'msg':err})
        else:
            data=User.objects.create(FName=fname,LName=lname,Address=address,Email=email,Password=paswd)
            return redirect("loginpage")

def LogInUser(request):
    emailid=request.POST['email']
    paswd=request.POST['pswd']
    user= User.objects.filter(Email=emailid)
    if len(user)>0 and user[0].Role=='Reception Admin':
        if user[0].Password == paswd:
            # detail=User.objects.get(FName=user[0].FName)
            request.session['id'] = user[0].id
            request.session['emailid'] = user[0].Email
            request.session['fname'] = user[0].FName
            return redirect("indexpage")
        else:
            err="Password is Incorrect !"
            return render(request,"Reception/login.html",{'msg':err})
    else:
        err="User Doesn't Exist !"
        return render(request,"Reception/login.html",{'msg':err})           

def LogOut(request):
    del request.session['id']
    del request.session['emailid']
    del request.session['fname']
    return redirect("loginpage")

# -----------------------  Registration / Log In / LogOut Start -----------------------
# ----------------------- AppointMent Section Start -----------------------
def BookAppointmentAdmin(request):
    if 'id' in request.session and 'emailid' in request.session:
        doctor=Doctor.objects.all().values()
        patient=Patients.objects.all().values()
        d={"patientdata":patient,"doctordata":doctor}
        return render(request,"Reception/book-appointment.html",d)
    else:
        return render(request,"Patients/Patient-login.html")

def AllAppointmentAdmin(request):
    if 'id' in request.session and 'emailid' in request.session:
            appointdetails=Appointments.objects.all()
            user=User.objects.get(id=request.session['id'])
            d={"data":user,"appointmentdata":appointdetails}
            return render(request,"Reception/All-Appointment.html",d)

def RequestAppointmentAdmin(request):
    if 'id' in request.session and 'emailid' in request.session:
        if request.method=='POST':
            patientinformation=request.POST['patientinfo']
            docinformation=request.POST['docterinfo']
            discription=request.POST['discription']
            appointmentdate=request.POST['appointmentdate']

            doctorid=docinformation.split()
            patientid=patientinformation.split()
            
            did=Doctor.objects.get(id=doctorid[0])
            pid=Patients.objects.get(id=patientid[0])
            appointment=Appointments.objects.create(PatientId=pid,DoctorId=did,AppointmentDate=appointmentdate,Discription=discription,Status="Approve")
            
            user=User.objects.get(id=request.session['id'])
            appointmentdata=Appointments.objects.all()
            d={"data":user,"appointmentdata":appointmentdata}
            return redirect("allappointmentadmin")
    else:
        return redirect("Patientlogin")


def ApproveAppointment(request,pk,st):
    if 'id' in request.session and 'emailid' in request.session:
        appointment=Appointments.objects.get(id=pk)
        user=User.objects.get(id=request.session['id'])
        appointment.Status = st
        appointment.save()
        return redirect("allappointmentadmin")
    return redirect("loginpage")
# ----------------------- AppointMent Section End -----------------------
# ----------------------- Forgot Password Section Start -----------------------
def ForgetPassword(request):
    return render(request,"Reception/forgot-password.html")

def EnterOtp(request):
    if request.method=='POST':
        emailid=request.POST['email']
        user=User.objects.filter(Email=emailid)
        if len(user)>0:
            did=User.objects.get(Email=emailid)
            sbj="Forget your Password"
            otp=""
            for i in range(6):
                otp+=str(randint(1,9))
            did.OTP =otp
            did.save()
            msg=f"You are OTP is {otp}"
            sender=settings.EMAIL_HOST_USER
            rl=[emailid,]
            send_mail(sbj,msg,sender,rl)
            return render(request,"Reception/forgot-password-OTP.html",{"data":did})
        else:
            err="Incorrect Email Id! Please Enter Again"
            return render(request,"Reception/forgot-password.html",{'msg':err})
    else:
        return render(request,"Reception/forgot-password.html")

def OTPVerify(request):
    if request.method=='POST':
        emailid=request.POST['email'] 
        otp2=request.POST['otp']
        did=User.objects.get(Email=emailid)
        if did.OTP==otp2:
            return render(request,"Reception/Change-Password.html",{"data":did}) 
        else:
            err="Incorrect OTP! Please Enter Again"
            return render(request,"Reception/forgot-password-OTP.html",{'msg':err})

def ChangePassword(request):
    if request.method=='POST':
        emailid=request.POST['email'] 
        newpswd=request.POST['newpswd']
        did=User.objects.get(Email=emailid)
        did.Password =newpswd
        did.save()
        
        sbj="Your Password is Changed Successfully. . ."
        msg="If you are not do this please contact our team"
        sender=settings.EMAIL_HOST_USER
        rl=[emailid,]
        send_mail(sbj,msg,sender,rl)
        err="Password Changed Successfully"
        if did.Role=="Reception Admin":
            return render(request,"Reception/login.html",{'msg':err})
        elif did.Role=="Doctor":
            did=Doctor.objects.get(Email=emailid)
            did.Password =newpswd
            did.save()
            return render(request,"Doctor/doctor-login.html",{'msg':err})
        elif did.Role=="Patient":
            did=Patients.objects.get(Email=emailid)
            did.Password =newpswd
            did.save()
            return render(request,"Patients/Patient-login.html",{'msg':err})
    else:
        return render(request,"Reception/forgot-password-OTP.html")

# ----------------------- Doctor Section Start -----------------------
def AllDoctors(request):
    if ('id' in request.session and 'emailid' in request.session):
        doctor=Doctor.objects.all()
        user=User.objects.get(id=request.session['id'])
        a,b,c='Pending',"Approve",'Reject'
        d={"data":user,"doctordata":doctor,"Pending":a,"Approve":b,'Reject':c}
        return render(request,"Reception/All-doctors.html",d)
    return redirect("loginpage")

def DocProfile(request,pk):
    if 'id' in request.session and 'emailid' in request.session:
        doctor=Doctor.objects.get(id=pk)
        user=User.objects.get(id=request.session['id'])
        d={"data":user,"doctordata":doctor}
    return render(request,"Reception/Doc-Profile.html",d)

def DocUpdate(request,pk):
    if request.method=='POST':
        did=Doctor.objects.get(id=pk)
        usid=User.objects.get(id=did.user.id)
        print(f"-----USID-->{usid}")     
        did.Fname=request.POST['fname'] if request.POST['fname'] else did.Fname
        did.Lname=request.POST['lname'] if request.POST['lname'] else did.Lname
        did.BirthDay=request.POST['dob'] if request.POST['dob'] else did.BirthDay
        did.Address=request.POST['address'] if request.POST['address'] else did.Address
        did.Phone_Number=request.POST['phone'] if request.POST['phone'] else did.Phone_Number
        did.Email=request.POST['email'] if request.POST['email'] else did.Email
        did.ProfilePic=request.FILES['propic'] if request.FILES['propic'] else did.ProfilePic
        did.save()

        usid.FName=request.POST['fname'] if request.POST['fname'] else usid.FName
        usid.LName=request.POST['lname'] if request.POST['lname'] else usid.LName
        usid.Email=request.POST['email'] if request.POST['email'] else usid.Email
        usid.Address=request.POST['address'] if request.POST['address'] else usid.Address
        usid.save()
        print(f"bdate-------------->",did.BirthDay)
        url = f"/Doc-Profile/{pk}/"
        return redirect(url)

def DocDelete(request,pk):
    did=Doctor.objects.get(id=pk)
    did.delete()
    usid=User.objects.get(id=did.user.id)
    usid.delete()
    return redirect("alldoctors")

def DoctorStatus(request):
    if 'id' in request.session and 'emailid' in request.session:
        doctor=Doctor.objects.all()
        user=User.objects.get(id=request.session['id'])
        d={"data":user,"doctordata":doctor}
        return render(request,"Reception/Approve-Doctor.html",d)

def DoctorApprove(request,pk,st):
    if 'id' in request.session and 'emailid' in request.session:
        doctor=Doctor.objects.get(id=pk)
        user=User.objects.get(id=request.session['id'])
        doctor.DStatus = st
        doctor.save()
        return redirect("alldoctors")
    return redirect("loginpage")

# ----------------------- Doctor Section End -----------------------
# ----------------------- Patient Section Start -----------------------
def AllPatients(request):
    if 'id' in request.session and 'emailid' in request.session:
        patient=Patients.objects.all()
        user=User.objects.get(id=request.session['id'])
        discharge=DischargePatients.objects.all()
        d={"data":user,"patientdata":patient,'dischargedata':discharge}
        return render(request,"Reception/All-patients.html",d)
    else:
        return render(request,"Reception/All-patients.html")

def PatientsProfile(request,pk):
    if 'id' in request.session and 'emailid' in request.session:
        patient=Patients.objects.get(id=pk)
        user=User.objects.get(id=request.session['id'])
        d={"data":user,"patientdata":patient}
    return render(request,"Reception/patient-prof.html",d)

def PatientUpdatePage(request,pk):
    patient=Patients.objects.get(id=pk)
    user=User.objects.get(id=request.session['id'])
    d={"data":user,"patientdata":patient}
    return render(request,"Reception/patient-update.html",d)

def PatientUpdate(request,pk):
    if request.method=='POST':
        pid=Patients.objects.get(id=pk)
        usid=User.objects.get(id=pid.user.id)
        print(f"-----USID-->{usid}")      
        pid.Fname=request.POST['fname'] if request.POST['fname'] else pid.Fname
        pid.Lname=request.POST['lname'] if request.POST['lname'] else pid.Lname
        pid.Symptoms=request.POST['symptoms'] if request.POST['symptoms'] else pid.Symptoms
        pid.Email=request.POST['email'] if request.POST['email'] else pid.Email
        pid.Phone_Number=request.POST['phone'] if request.POST['phone'] else pid.Phone_Number
        pid.Age=request.POST['age'] if request.POST['age'] else pid.Age
        pid.Address=request.POST['address'] if request.POST['address'] else pid.Address
        pid.save()

        usid.FName=request.POST['fname'] if request.POST['fname'] else usid.FName
        usid.LName=request.POST['lname'] if request.POST['lname'] else usid.LName
        usid.Email=request.POST['email'] if request.POST['email'] else usid.Email
        usid.Address=request.POST['address'] if request.POST['address'] else usid.Address
        usid.save()
        url = f"/Patients-Profile/{pk}/"
        return redirect(url)

def PatientDelete(request,pk):
    pid=Patients.objects.get(id=pk)
    pid.delete()
    usid=User.objects.get(id=pid.user.id)
    usid.delete()
    return redirect("allpatients")

def PatientApprove(request,pk,st):
    if 'id' in request.session and 'emailid' in request.session:
        patient=Patients.objects.get(id=pk)
        user=User.objects.get(id=request.session['id'])
        patient.status = st
        patient.save()
        return redirect("allpatients")
    return redirect("loginpage")

# ----------------------- Patient Section End -----------------------
# ----------------------- Invoice | Payment | Receipt Section Start -----------------------
def AddPatientBill(request):
    if 'id' in request.session and 'emailid' in request.session:
        user=User.objects.get(id=request.session['id'])
    doctor=Doctor.objects.all()
    patients=Patients.objects.all()
    billnum=(DischargePatients.objects.order_by('-Bill_Number')[0].Bill_Number)+1
    a=False
    d={"doctordata":doctor,"patientdata":patients,"data":user,"billnum":billnum,"a":a}
    return render(request,"Reception/add-payment.html",d)

def SelectedBillIndex(request,pk):
    if 'id' in request.session and 'emailid' in request.session:
        user=User.objects.get(id=request.session['id'])
    patients=Patients.objects.get(id=pk)
    doctor=Doctor.objects.get(id=patients.DoctorId.id)
    billnum=(DischargePatients.objects.order_by('-Bill_Number')[0].Bill_Number)+1
    a=True
    d={"doctordata":doctor,"patientdata":patients,"data":user,"billnum":billnum,"a":a}
    return render(request,"Reception/add-payment.html",d)

def BillData(request):
    if 'id' in request.session and 'emailid' in request.session:
        user=User.objects.get(id=request.session['id'])
        if request.method=="POST":
            patientinfo = request.POST['patientinfo']
            docinfo = request.POST['docterinfo']
            paydate = request.POST['Paymentdate']
            rcharge = int(request.POST['roomcharge'])
            dcharge = int(request.POST['doccharge'])
            mcharge = int(request.POST['medicinecharge'])
            echarge = int(request.POST['extracharge'])
            
            doctorid=docinfo.split()
            patientid=patientinfo.split()
            did=Doctor.objects.get(id=doctorid[0])
            pid=Patients.objects.get(id=patientid[0])
            
            days=(date.today()-pid.Created)
            d =days.days
            Total = (int(request.POST['roomcharge'])*int(d)) + int(request.POST['doccharge']) + int(request.POST['medicinecharge']) + int(request.POST['extracharge'])
            billnum=(DischargePatients.objects.order_by('-Bill_Number')[0].Bill_Number)+1
            
            Discharge=DischargePatients.objects.create(user=user,PatientId=pid,DoctorId=did,RoomCharge=rcharge*d,MedicineCost=mcharge,Bill_Number=billnum,PaymentDate=paydate,DoctorFee=dcharge,OtherCharge=echarge,Total=Total)
            pid.status = "Discharge"
            pid.save()
            
            dic={
                'pid':pid.id,
                'name':pid.Fname + " " + pid.Lname,
                'mobile':pid.Phone_Number,
                'address':pid.Address,
                'admitDate':pid.Created,
                'assignedDoctorName':did.Fname,
                'day':d,
                'todayDate':date.today(),
                'symptoms':pid.Symptoms,
                'roomCharge':rcharge*d,
                'doctorFee':dcharge,
                'medicineCost':mcharge,
                'OtherCharge':echarge,
                'total':Total
            }
        return render(request,"Reception/Patient-Final-Bill.html",dic)

def AllPayment(request):
    if 'id' in request.session and 'emailid' in request.session:
        user=User.objects.get(id=request.session['id'])
        bill=DischargePatients.objects.all()
        d={"data":user,"bill":bill}
    return render(request,"Reception/all-payment.html",d)

# ----------------------- Invoice | Payment | Receipt Section End -----------------------
# ----------------------- Discharge Patient Bill (pdf) Download & Printing -----------------------

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return

def DownloadPDF(request,pk):
    try:
        dischargedetails=DischargePatients.objects.get(PatientId=pk)
        pid=Patients.objects.get(id=pk)
        days=(date.today()-pid.Created)
        d =days.days
        dic={
                    'pid':pid.id,
                    'name':pid.Fname + " " + pid.Lname,
                    'mobile':pid.Phone_Number,
                    'address':pid.Address,
                    'admitDate':pid.Created,
                    'assignedDoctorName':dischargedetails.DoctorId.Fname,
                    'day':d,
                    'todayDate':date.today(),
                    'symptoms':pid.Symptoms,
                    'roomCharge':dischargedetails.RoomCharge*d,
                    'doctorFee':dischargedetails.DoctorFee,
                    'medicineCost':dischargedetails.MedicineCost,
                    'OtherCharge':dischargedetails.OtherCharge,
                    'total':dischargedetails.Total
                }
        return render_to_pdf('Reception/Download_Bill.html',dic)
    except:
        if 'Patientid' in request.session and 'Patientemail' in request.session:
            return render(request,'Reception/Patient-Final-Bill.html')