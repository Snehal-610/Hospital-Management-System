from django.db import models
from Reception.models import *

# Create your models here.
class Doctor(models.Model):
    GChoice=[('Gender','Gender'),('Male','Male'),('Female','Female')]
    SChoice=[('Pending','Pending'),('Approve','Approve'),('Reject','Reject')]
    departments=[('Departments','Departments'),('Cardiologist','Cardiologist'),
                ('Dermatologists','Dermatologists'),
                ('Emergency Medicine Specialists','Emergency Medicine Specialists'),
                ('Allergists/Immunologists','Allergists/Immunologists'),
                ('Anesthesiologists','Anesthesiologists'),
                ('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
                ]
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Fname=models.CharField(max_length=50)
    Lname=models.CharField(max_length=50)
    Role=models.CharField(max_length=50,default="Doctor")
    BirthDay=models.DateField(auto_now_add=True)
    Address=models.CharField(max_length=300,null=True)
    Phone_Number = models.CharField(max_length=12)
    Gender=models.CharField(max_length=6,choices=GChoice,default='Gender')
    Department= models.CharField(max_length=150,choices=departments,default='Departments')
    Email=models.EmailField(max_length=100,unique=True)
    Password=models.CharField(max_length=100)
    ProfilePic=models.ImageField(upload_to="Doctor/Profile/",default="none.jpg")
    Created = models.DateTimeField(auto_now_add=True)
    DStatus=models.CharField(max_length=100,choices=SChoice,default='Pending')

    def __str__(self):
        return self.Fname