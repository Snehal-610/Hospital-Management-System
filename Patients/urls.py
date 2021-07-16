from django.contrib import admin
from django.urls import path
from Patients import views


urlpatterns = [
    path('',views.PatientLogInPage,name="Patientlogin"),
    path('Patient-Index',views.PatientIndex,name="Patientindex"),
    path('Patient-SignUp',views.PatientSignUp,name="PatientSignUp"),
    path('Patient-LogUser',views.PatientLogInUser,name="patientLogUser"),
    path('Patient-RegUser',views.PatientRegisterUser,name="patientreguser"),
    path('Patient-LogOut',views.PatientLogOutUser,name="patientlogout"),
    
    path('Patient-Profile',views.PatientProfile,name="patientprofile"),
    path('Patient-Upadate',views.PatientUpdate,name="patientupdate"),
    path('Patient-Appointment',views.PatientAppointment,name="patientappointment"),
    path("Book-Appointment/",views.BookAppointment,name="bookappointment"), 
    path('Request-Appointment',views.RequestAppointment,name="requestappointment"),
]