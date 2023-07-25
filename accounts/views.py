
from django.contrib import messages,auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from .forms import * 
from adminapp.models import *
from . import helper
from payment.models import *
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
        
    return render(request,'store_templates/signup.html',{'sub': Subcategory.objects.all()})



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
            try:
                w = Wallet.objects.get(user=user)
                if w:
                    pass
                else:
                    raise Exception
            except:
               w =  Wallet.objects.create(user=user,wallet_amount=0)

            print(w)
            messages.info(request,'Logged in succesfully')
            
            return render(request,'store_templates/homepage.html',{'user':user})
        else:
            print("else")
            messages.error(request,'Invalid credentials')
            return redirect('signin')
        
    return render(request,'store_templates/signin.html',{'sub': Subcategory.objects.all()})


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
                return render(request, 'store_templates/sendotp.html',{'message':message})
    return render(request, 'store_templates/sendotp.html',{'form':form,'sub': Subcategory.objects.all()})



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
                    return render(request,'store_templates/homepage.html',{'name':name})
                return redirect('homepage')
            else:
                print("error")
    else:
        form = OTPverificationForm()
    return render(request, 'store_templates/verify_otp.html', {'form': form,'sub': Subcategory.objects.all()})



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





# forgot password
def forgotPassword(request):
    print("entered forgotpassword number")
    global mobile_number_forgotPassword
    if request.method == 'POST':
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = request.POST.get('phone_number')
        # checking the null case
        if mobile_number_forgotPassword == '':
            messages.warning(request, 'You must enter a mobile number')
            return redirect('forgotPassword')
   
        
        user = CustomUser.objects.filter(phone_number=mobile_number_forgotPassword)
        if user:  #if user exists
            helper.send('+91' + str(mobile_number_forgotPassword))
            return redirect('forgotPassword_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgotPassword')
            
    return render(request, 'store_templates/forgot_password.html')


def forgotPassword_otp(request):
    print("verify forgotpassword otp")
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        form = OTPverificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('OTP')
        # otp = request.POST.get('otp')
        if helper.check('+91'+ str(mobile_number), otp):
            user = CustomUser.objects.get(phone_number=mobile_number)
            if user:
                print(user,"this is user")
                return redirect('resetPassword')
        else:
            messages.warning(request,'Invalid OTP')
            return redirect('enter_otp')
    else:
        form = OTPverificationForm()
        
    return render(request,'store_templates/forgotPassword_otp.html', {'form':form})


def resetPassword(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        print(str(password1)+' '+str(password2)) #checking
        
        if password1 == password2:
            user = CustomUser.objects.get(phone_number=mobile_number)
            print(user)
            print('old password  : ' +str(user.password))
            
            user.set_password(password1)
            user.save()

            print('new password  : ' +str(user.password))
            messages.success(request, 'Password changed successfully')
            return redirect('signin')
        else:
            messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('resetPassword')
    
    return render(request, 'store_templates/resetPassword.html')


# user profile function
def userprofile(request):
    user=request.user
    address = user.addresses.all()
   
    if address:
        address_added = True
    else:
        address_added = False

    context = {
        
        'address_added': address_added,
        'address': address,
        'sub': Subcategory.objects.all()
    }

    return render(request, 'store_templates/userprofile.html', context)



# add address html rendering
def add_address(request):
  user=request.user
  user_profile = UserProfile()
  if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            print("valid")
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            pincode = form.cleaned_data['pincode']
            status = request.POST['my_checkbox']
            print(status)
            user_profile = UserProfile(user=user,address_line_1=address_line_1,address_line_2=address_line_2,city=city,state=state,country=country,pincode=pincode,status=status)
            print(user_profile.status)
            user_profile.save()
            return redirect('userprofile')
  else:
        form = UserProfileForm()

  context = {
        'form': form,
        
        'user_profile': user_profile,
        'sub': Subcategory.objects.all()
    }
  return render(request,'store_templates/add_address.html',context)


# edit user profile address
def edit_address(request,id):
    print(id)
    user_address = request.user.addresses.get(id=id)
    print(user_address)
    form = UserProfileForm(instance=user_address)
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            print("valid")
            user_address.address_line_1 = form.cleaned_data['address_line_1']
            user_address.address_line_2 = form.cleaned_data['address_line_2']
            user_address.city = form.cleaned_data['city']
            user_address.state = form.cleaned_data['state']
            user_address.country = form.cleaned_data['country']
            user_address.pincode = form.cleaned_data['pincode']
            status = request.POST['my_checkbox']
            print(status)
            user_address.status = status
            user_address.save()
            return redirect('userprofile')
    context = {'form':form,
               'sub': Subcategory.objects.all()}
    return render(request,'store_templates/edit_address.html',context)



# delete address of user
def delete_address(request,id):
    print(id)
    user_address = request.user.addresses.get(id=id)
    print(user_address)
    user_address.delete()
    return redirect('userprofile')



# edit user signup details
def edit_user_details(request):
    user = request.user
    if request.method == 'POST':
        form = Aforms(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile')  # Replace 'profile' with the URL name of the user's profile page
    else:
        form = Aforms(instance=user)
    
    context = {
        'form': form,
        'sub': Subcategory.objects.all()
    }
    return render(request, 'store_templates/edit_user_detials.html', context)
