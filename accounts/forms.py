from django import forms
from .models import CustomUser,UserProfile
from django.contrib.auth.forms import UserCreationForm
# from phonenumber_field.formfields import PhoneNumberField



class Aforms(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','name','phone_number']
        widgets = {
            
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'name': forms.TextInput(attrs={'class':"form-control"}),
            'phone_number': forms.TextInput(attrs={'class':"form-control"}),
           
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        }


# phone number input form for user to send otp
class OTPForm(forms.Form):
    phone_number = forms.CharField(max_length=15,required=True)



# otp entering input form for user
class OTPverificationForm(forms.Form):
    OTP = forms.CharField(max_length=6)


# userprofile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address_line_1','address_line_2', 'city','state','country','pincode']
        widgets = {
            
            'address_line_1': forms.TextInput(attrs={'class': "form-control"}),
            'address_line_2': forms.TextInput(attrs={'class':"form-control"}),
            'city': forms.TextInput(attrs={'class':"form-control"}),
            'state': forms.TextInput(attrs={'class': "form-control"}),
            'country': forms.TextInput(attrs={'class':"form-control"}),
            'pincode': forms.TextInput(attrs={'class':"form-control"}),
            
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        }
    