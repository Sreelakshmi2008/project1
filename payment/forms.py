from django import forms

from .models import *

class razorpayForm(forms.Form):
   
    amount = forms.FloatField(required=True)
    
    class Meta:
          widgets = {
            
            
            'amount': forms.NumberInput(attrs={'class':"form-control"}),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
        }
    

class couponForm(forms.ModelForm):
     class Meta:
          model = Coupon
          fields = ['coupon_code','discount_price','minimum_amount']
          widgets = {
            
            
            'coupon_code': forms.TextInput(attrs={'class': "form-control", 'background-color': '#ff0000'}),

            'discount_price': forms.NumberInput(attrs={'class':"form-control"}),
            'minimum_amount': forms.NumberInput(attrs={'class':"form-control"}),
           
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        }