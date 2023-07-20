from django.db import models
from mystore.models import *
from accounts.models import *
from adminapp.models import *



# Create your models here.


class SalesReport(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)

   
    def __str__(self):
        return f"Sales Report - Product #{self.product.name}"


