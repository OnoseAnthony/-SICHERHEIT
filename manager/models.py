from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.

class User(AbstractUser):
    login_passphrase = models.CharField(max_length = 15)



class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile', null=True)
    password =  models.CharField(max_length = 20)
    application_service_name =  models.CharField(max_length = 12, default='Papercode Technologies')
    application_service_url =  models.CharField(max_length = 30, default="https://tech.papercodetech.com")
    registered_username =  models.CharField(max_length = 30, blank = True, null = True)
    registered_email_address =  models.CharField(max_length = 30, blank = True, null = True)
    qrcode_image = models.ImageField(upload_to='qrcode', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        ordering = ("registered_email_address",)

    def __str__(self):
        return f"{self.application_service_name} - {self.application_service_url}"
