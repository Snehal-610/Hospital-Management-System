from django.db import models
# Create your models here.
class User(models.Model):
    FName=models.CharField(max_length=100)
    LName=models.CharField(max_length=100)
    Role=models.CharField(max_length=50,default="Reception Admin")
    Address=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100,unique=True)
    Password=models.CharField(max_length=100)
    RegistrationDate=models.DateTimeField(auto_now_add=True)
    OTP=models.CharField(max_length=6,null=True)
    
    def __str__(self):
        return self.Role + " --> " + self.FName + " " + self.LName

