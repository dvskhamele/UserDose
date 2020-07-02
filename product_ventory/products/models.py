from django.db import models
from product_ventory.users.models import User
from django.utils import timezone

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    quantity = models.IntegerField()
    price = models.IntegerField()
    available = models.BooleanField()
    stock = models.CharField(max_length=30)
    total = models.IntegerField()
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    document = models.FileField(upload_to='',null = True)


