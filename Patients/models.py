import Doctor
from django.db import models
from Reception.models import *
from Doctor.models import Doctor

# Create your models here.
class Patients(models.Model):
    GChoice=[('Gender','Gender'),('Male','Male'),('Female','Female')]
    SChoice=[('Pending','Pending'),('Approve','Approve'),('Reject','Reject'),('Discharge','Discharge')]
    
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    DoctorId=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    Fname=models.CharField(max_length=50)
    Lname=models.CharField(max_length=50)
    Age=models.PositiveIntegerField()
    Role=models.CharField(max_length=50,default="Patient")
    Symptoms=models.CharField(max_length=100)
    Address=models.CharField(max_length=300,null=True)
    Phone_Number = models.CharField(max_length=12)
    Gender=models.CharField(max_length=6,choices=GChoice,default='Gender')
    Email=models.EmailField(max_length=100,unique=True)
    Password=models.CharField(max_length=100)
    Created = models.DateField(auto_now_add=True)
    status=models.CharField(max_length=30,choices=SChoice,default='Pending',null=True)
    def __str__(self):
        return self.Fname

class Appointments(models.Model):
    SChoice=[('Pending','Pending'),('Approve','Approve'),('Reject','Reject')]

    PatientId=models.ForeignKey(Patients,on_delete=models.CASCADE,null=True)
    DoctorId=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    AppointmentDate=models.DateField(auto_now=True)
    Discription=models.TextField(max_length=500)
    Status=models.CharField(max_length=30,choices=SChoice,default='Pending',null=True)

class DischargePatients(models.Model):
    Bill_Number=models.BigAutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    PatientId=models.ForeignKey(Patients,on_delete=models.CASCADE,null=True)
    DoctorId=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
    PaymentDate=models.DateField(auto_now_add=True,null=False)
    RoomCharge=models.PositiveIntegerField(null=False,default=0)
    MedicineCost=models.PositiveIntegerField(null=False,default=0)
    DoctorFee=models.PositiveIntegerField(null=False,default=0)
    OtherCharge=models.PositiveIntegerField(null=False)
    Total=models.PositiveIntegerField(null=False,default=0)