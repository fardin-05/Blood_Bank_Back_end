from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone
class CustomUser(AbstractUser):
    username=None
    first_name = models.CharField(max_length=100)
    last_name =models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    address= models.TextField(blank=True, null=True)
    phone_number=models.CharField(max_length=15, blank=True, null=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=5,
        choices=[
            ('A+','A+'),('A-','A-'),
            ('B+','B+'),('B-','B-'),
            ('AB+','AB+'),('AB-','AB-'),
            ('O+','O+'),('O-','O-'),
        ],
        null=True, blank=True
    )
    availability = models.BooleanField(
        default=True,
        help_text='Available for Blood Donation')
    
    last_donation = models.DateField(null=True, blank=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects= CustomUserManager()
    def __str__(self):
        return self.email
    