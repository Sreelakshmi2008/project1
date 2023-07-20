from django import forms
from .models import *



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user','payment','shipping_address','order_total']



class CancelOrderForm(forms.ModelForm):
    class Meta:
        model = CancelOrder
        fields = ['cancel_reason']

    def clean_cancel_reason(self):
        cancel_reason = self.cleaned_data.get('cancel_reason')
        if cancel_reason == '':
            raise forms.ValidationError('Please select a reason for cancelling the order.')
        return cancel_reason

