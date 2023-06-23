from django.db import models
from accounts.models import CustomUser
from adminapp.models import Product,Size,Color,ProductVariant,ProductColor


# creating a cart for a user

class Cart(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    products = models.ManyToManyField(Product, through='CartItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
    def get_total_price(self):
        return sum(item.get_subtotal() for item in self.cart_items.all())
    
    def get_total_products(self):
        return sum(item.quantity for item in self.cart_items.all())
    
    # def get_total_quantity(self):
    #     return sum(item.quantity for item in self.cart_items.all())
    
    # def get_total_offerprice(self):
    #     return sum(item.get_subtotalprice() for item in self.cart_items.all())
    
    # def get_price_difference(self):
    #     return self.get_total_price() - self.get_total_offerprice()
    
    # def get_shipping_charge(self):
    #     total_amount = self.get_total_price()
    #     if total_amount > 1000:
    #         return 0
    #     else:
    #         return 200
        
    # def get_total(self):
    #     return self.get_total_price() - self.get_shipping_charge() - self.get_price_difference()
    

# to add items to users cart
class CartItem(models.Model):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='cart_item_product') 
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    product_color = models.ForeignKey(ProductColor, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)

    
    def get_subtotal(self):
        return self.product_variant.price * self.quantity
    

