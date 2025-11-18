from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Restaurant(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=150)
    img = models.ImageField(upload_to='restaurant/')

    def __str__(self):
        return self.name


class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    table_num = models.CharField()
    seats = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Table {self.table_num}"


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='menu_images')


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    table = models.ForeignKey(Table,on_delete=models.CASCADE)
    guests = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sent_messages")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="received_messages")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']