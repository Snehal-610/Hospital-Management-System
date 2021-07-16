from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.DoctorLogInPage,name="Doclogin"),
    path('Doctor-Index',views.DoctorIndex,name="Docindex"),
    path('Doctor-SignUp',views.DoctorSignUp,name="DocSignUp"),
    path('Doctor-LogUser',views.DoctorLogInUser,name="DocLogUser"),
    path('Doctor-RegUser',views.DoctorRegisterUser,name="Docreguser"),
    path('Doctor-LogOut',views.DoctorLogOutUser,name="Doclogout"),
    path('Doctor-Profile',views.DoctorProfile,name="Docprofile"),
    path('Doctor-Upadate',views.DoctorUpdate,name="Docupdate"),
    path('Doctor-Appointments',views.DoctorAppointment,name="doctorappointment"),
    path('Doctor-Patients',views.DoctorPatients,name="doctorpatients"),
]