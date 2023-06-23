
from django.contrib import messages,auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CustomUser,UserProfile
from django.db.models import Q
from .forms import OTPForm,OTPverificationForm,UserProfileForm  
from . import helper

# Create your views here.


#user signup and signin

# signup for users
def signup(request):
    print("entered")
    email = request.session.get('email')
   
    if email:
        return redirect('homepage')
    if request.method == 'POST':
        print("post")
        email = request.POST['email']
        print(email)
        name = request.POST['name']
        print(name)
        phone_number = request.POST['phone_number']
        print(phone_number)
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        print(pass1,pass2)
        if pass1 == pass2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,'User already exists')
                return redirect('signup')
            else:
                print("else")
                user = CustomUser.objects.create_user(email=email,name=name,phone_number=phone_number, password=pass1)
                print(user)
                user.save()

                return redirect('signin')
            
        else:
            messages.info(request,'Passwords do not match')
            return redirect('signup')
        
    return render(request,'store_templates\signup.html')



# signin for users using password
def signin(request):
    print("entered signin")
    
    email = request.session.get('email')
   
    if email:
        return redirect('homepage')
    if request.method == 'POST':
        print("entered signin post")
        email = request.POST['email']
        print(email)
        password = request.POST['pass1']
        print(password)
        user = authenticate(email=email,password=password)
        print(user)
        if user is not None:
            print("if")
            name = user.name
            login(request,user)
            request.session['email']=email
            messages.info(request,'Logged in succesfully')
            
            return render(request,'store_templates\homepage.html',{'name':name})
        else:
            print("else")
            messages.error(request,'Invalid credentials')
            return redirect('signin')
        
    return render(request,'store_templates\signin.html')


# signout from account of user
def signout(request):
    logout(request)
    request.session.flush()
    messages.success(request,"Logged out succesfully")
    return redirect('homepage')


#otp-login for users - sending otp to their phone number
def otp_login(request):
    form = OTPForm()
    if request.method == "POST":
        form = OTPForm(request.POST)
        phone = '+91'+  str(request.POST['phone_number'])
        if check_phone_number(request.POST['phone_number']):
            user = email_password(request.POST['phone_number'])
            if user:
                helper.send(phone)
                request.session['user_email'] = user.email
                print(user.email)
                user.is_verified = True
                user.is_active = True
                request.session['phone'] = phone
                return redirect('verifyotp')
            else:
                message = "Please register first"
                return render(request, 'store_templates\sendotp.html',{'message':message})
    return render(request, 'store_templates\sendotp.html',{'form':form})



#otp-login for users - verifying th entered otp
def verify_otp(request):
    if request.method == 'POST':
        form = OTPverificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('OTP')
            phone_no = request.session.get('phone')

            if helper.check(phone_no, code):
                user = CustomUser.objects.get(email = request.session.get('user_email'))
                print(user)
                userobj = CustomUser.objects.filter(email = request.session.get('user_email'))
                print(userobj)
                if userobj is not None and user.is_active and user.is_superuser == False:
                    login(request, user)
                    name=user.name
                    return render(request,'store_templates\homepage.html',{'name':name})
                return redirect('homepage')
            else:
                print("error")
    else:
        form = OTPverificationForm()
    return render(request, 'store_templates/verify_otp.html', {'form': form})



# finding user email with given phonenumber
def email_password(phone):
    user = CustomUser.objects.filter(phone_number=phone).first()
    print(user)
    return user

# check whether user with given phone number exist or not
def check_phone_number(phone_number):
    try:
        phone_number = CustomUser.objects.filter(phone_number=phone_number)
        print(phone_number)
        return True
    except CustomUser.DoesNotExist:
        return False



# user profile function
def userprofile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if user_profile.address_line_1:
        address_added = True
    else:
        address_added = False

    context = {
        
        'address_added': address_added,
        'user_profile': user_profile
    }

    return render(request, 'store_templates/userprofile.html', context)



# add address html rendering
def add_address(request):
  user_profile = UserProfile.objects.get(user=request.user)

  if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile.address_line_1 = form.cleaned_data['address_line_1']
            user_profile.address_line_2 = form.cleaned_data['address_line_2']
            user_profile.city = form.cleaned_data['city']
            user_profile.state = form.cleaned_data['state']
            user_profile.country = form.cleaned_data['country']
            user_profile.pincode = form.cleaned_data['pincode']
            user_profile.save()
            return redirect('userprofile')
  else:
        form = UserProfileForm()

  context = {
        'form': form,
        
        'user_profile': user_profile
    }
  return render(request,'store_templates/add_address.html',context)


# edit user profile address
def edit_address(request):
    user_address = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=user_address)
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_address.address_line_1 = form.cleaned_data['address_line_1']
            user_address.address_line_2 = form.cleaned_data['address_line_2']
            user_address.city = form.cleaned_data['city']
            user_address.state = form.cleaned_data['state']
            user_address.country = form.cleaned_data['country']
            user_address.pincode = form.cleaned_data['pincode']
            user_address.save()
            return redirect('userprofile')
    context = {'form':form}
    return render(request,'store_templates/edit_address.html',context)



# delete address of user
def delete_address(request):
     user_address = UserProfile.objects.get(user=request.user)
     user_address.delete()
     return redirect('userprofile')
