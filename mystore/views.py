from django.shortcuts import render,redirect
from adminapp.models import Product,Category,Size,Subcategory,ProductColor,Color,ProductVariant
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import UserProfile
from cart.models import Cart,CartItem


# Create your views here.


# store homepage display
def homepage(request):
   product = Product.objects.all()
   sub = Subcategory.objects.all()
   return render(request,'store_templates\homepage.html',{'product':product,'sub':sub})


# menscollection html rendering
def menscollection(request):
   product = Product.objects.filter(category_id=1)
   sub = Subcategory.objects.all()
   return render(request,'store_templates\menscollection.html',{'product':product,'sub':sub})


# womencollection html rendering
def womencollection(request):
   product = Product.objects.filter(category_id=2)
   sub = Subcategory.objects.all()
   return render(request,'store_templates\womencollection.html',{'product':product,'sub':sub})


# product individual page 
def product_details(request,id):
  product = Product.objects.get(pk=id)    
  sub = Subcategory.objects.all()
  return render(request,'store_templates\product_details.html',{'product':product,'sub':sub})


# by sub category showing producst for user
def subcategory_filtering(request,id):
   sub = Subcategory.objects.all()
   sub_name = Subcategory.objects.get(pk=id).name
   product = Product.objects.filter(subcategory_id=id)
   return render(request,'store_templates\subcategory_filtering.html',{'product':product,'sub_name':sub_name,'sub':sub})



# check out page
def checkout_page(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if user_profile.address_line_1:
        address_added = True
    else:
        address_added = False

    context = {
        
        'address_added': address_added,
        'user_profile': user_profile
    }
    return render(request,'store_templates\checkout.html',context)




# order summary page
def order_summary(request):
   cart = Cart.objects.get(user=request.user)
   cart_items = CartItem.objects.all()
   sum = cart.get_total_price()
   total = cart.get_total_products()
   context = {
                    'cart_items': cart_items,
                    'cart': cart,
                    'sum':sum,
                    'total':total
                }
   return render(request,'store_templates\order_summary.html',context)