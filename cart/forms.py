from django import forms
from .models import Cart,CartItem



# users cart form
class cartForm(forms.ModelForm):
    class Meta:
        model =Cart
        fields = ['user','products','created_at','updated_at']
        

# cart items form
class cart_itemForm(forms.ModelForm):
    class Meta:
        model =CartItem
        fields = ['user','cart','product','product_variant','product_color','quantity','is_active']
        