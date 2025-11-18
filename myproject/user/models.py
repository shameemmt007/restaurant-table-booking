from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
        

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin','Admin'),
        ('restaurants','Restaurants'),
        ('customer','Customer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='customer')


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    addresses = models.CharField(max_length=100,null=True)
    description = models.TextField()
    profile_pic = models.ImageField(upload_to='profile')
