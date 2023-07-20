from django.db import models
from mystore.models import *
from accounts.models import *
from adminapp.models import *

from django.utils import timezone
from django.db.models.signals import post_save
from payment.models import Payment,Rewards,Coupon,Wallet
# Create your models here.




class Order(models.Model):
    STATUS = {
        ('New','New'),
        ('pending','pending'),
        ('processed','processed'),
        ('out for shipping','out for shipping'),
        ('canceled','canceled'),
        ('delivered','delivered'),
    }
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    payment =  models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,related_name='user_payment_details')
    order_number = models.CharField(max_length=30,null=True)
    shipping_address =  models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    
    order_total = models.FloatField()
    status = models.CharField(max_length=100,choices=STATUS,default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.order_number}-{self.user.name}"
    
class OrderItem(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE, null=True)
    product_variant=models.ForeignKey(ProductVariant,on_delete=models.SET_NULL,null=True)
    product_color=models.ForeignKey(ProductColor,on_delete=models.SET_NULL,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,related_name='myorders')
    quantity=models.IntegerField(default=0, null=True,blank=True)
    date_added=models.DateTimeField(default=timezone.localtime)
    ordered=models.BooleanField(default=False)


    def __str__(self):
        return f"{self.product.name}-{self.order}"
    

    @property
    def order_product_total(self):
        return self.quantity*self.product_variant.price


class CancelOrder(models.Model):
    reasons = {
        ('Wrong Size','Wrong Size'),
        ('Other reasons','Other reasons'),

    }
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    cancel_reason = models.CharField(max_length=100,choices=reasons)



# to save to cashback-amount automatically when number of orders of user exceeds 10
@receiver(post_save, sender=Order)  
def update_cashback_amount(sender, instance, **kwargs):
    # Check if the user has more than 10 orders
    user_orders = Order.objects.filter(user=instance.user)
    if user_orders.count() % 10 == 0:
        # Calculate the amount to be added (you can adjust this as needed)
        cashback_to_add = 10.00

        # Retrieve the user's Rewards instance or create one if it doesn't exist yet
        rewards, created = Rewards.objects.get_or_create(user=instance.user)

        # Update the cashback_amount
        rewards.cashback_amount = float(rewards.cashback_amount) + float(cashback_to_add)
        rewards.save()
