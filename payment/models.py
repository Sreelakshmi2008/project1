from django.db import models
from mystore.models import *
from accounts.models import *
from adminapp.models import *



# Create your models here.

class Payment(models.Model):
    payment_choices=(
        ('COD','COD'),
        
        ('Razorpay','Razorpay'),
         ('Wallet','Wallet'),
        
    )
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100,choices=payment_choices)
    amount_paid = models.CharField(max_length=100)
    razorpay_order_id = models.CharField(max_length=100,null=True)
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name}--{self.payment_method}--{self.amount_paid}--{self.razorpay_order_id}--{self.status}"
    






# coupon model
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)  
 


#  wallet implementation
class Wallet(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    wallet_amount = models.DecimalField(max_digits=10,decimal_places=2)



# rewards for user
class Rewards(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    cashback_amount = models.DecimalField(max_digits=10,decimal_places=2)
    


