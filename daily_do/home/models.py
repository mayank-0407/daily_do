from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class OTP(models.Model):
    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True, blank=True)
    otp_code=models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.otp_code
    
class Works(models.Model):
    user=models.ForeignKey(User, on_delete= models.CASCADE ,null=True, blank=True)
    todo=models.TextField(null=True)
    start_date=models.DateField(null=True)
    end_date=models.DateField(null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)