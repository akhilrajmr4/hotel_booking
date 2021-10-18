from django.core.validators import RegexValidator
from django.db import models


# Create your models here.

class hotel_details(models.Model):
    Hotel_name = models.CharField(max_length=254)
    Email = models.EmailField(max_length=254)
    Phone_number = models.CharField(max_length=12)
    Address = models.CharField(max_length=254)
    Password = models.CharField(max_length=255)
    Image = models.ImageField(upload_to="images/")

