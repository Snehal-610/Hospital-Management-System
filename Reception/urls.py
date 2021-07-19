from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.IndexPage, name="indexpage"),
    path('LogIn-Page/', views.LogInPage, name="loginpage"),
    path('Register-Page/', views.RegisterPage, name="registerpage"),
    path("Register-User/",views.RegisterUser,name="registeruser"),
    path("LogIn-User/",views.LogInUser,name="loginuser"),
    path("LogOut-User/",views.LogOut,name="logoutuser"),

    path("All-Appointment-Admin/",views.AllAppointmentAdmin,name="allappointmentadmin"),   
    path("Book-Appointment-Admin/",views.BookAppointmentAdmin,name="bookappointmentadmin"),   
    path("Request-Appointment-Admin/",views.RequestAppointmentAdmin,name="requestappointmentadmin"),   
    path('Approve-Appointment/<int:pk><str:st>/',views.ApproveAppointment,name="approveappointment"),
    
    path('Forgot-Password/', views.ForgetPassword, name="forgetpswd"),
    path('Enter-Otp/',views.EnterOtp,name="EnterOtp"),
    path('OTP-Verify/',views.OTPVerify,name="otpverify"),
    path('Change-Password/',views.ChangePassword,name="changepassword"),
    
    path("All-Doctors/",views.AllDoctors,name="alldoctors"),
    path('Doc-Profile/<int:pk>/',views.DocProfile,name="docprofile"),
    path('Doc-Update/<int:pk>/',views.DocUpdate,name="docupdate"),
    path('Doc-Delete/<int:pk>/',views.DocDelete,name="docdelete"),
    path("Doctor-Status/",views.DoctorStatus,name="doctorstatus"),
    path('Doc-Approve/<int:pk><str:st>/',views.DoctorApprove,name="docapprove"),

    path("All-Patients/",views.AllPatients,name="allpatients"), 
    path("Patients-UpdatePage/<int:pk>/",views.PatientUpdatePage,name="patientupdatepage"), 
    path('Patients-Profile/<int:pk>/',views.PatientsProfile,name="patientsprofile"),
    path("Patients-Delete/<int:pk>/",views.PatientDelete,name="patientsdelete"), 
    path("Patients-Update/<int:pk>/",views.PatientUpdate,name="patientsupdate"), 
    path('Patient-Approve/<int:pk><str:st>/',views.PatientApprove,name="patientapprove"),

    path("Add-Patient-Bill/",views.AddPatientBill,name="patientbill"),
    path("Selected-Patient-Bill/<int:pk>/",views.SelectedBillIndex,name="Selectedpatientbill"),
    path("Bill-Data/",views.BillData,name="billdata"),
    path("Patient-Final-Bill/",views.PatientFinalBill,name="patientfinalbill"),
    path("All-Payment/",views.AllPayment,name="allpayment"),
]