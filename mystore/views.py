from django.shortcuts import render,redirect,HttpResponse
from adminapp.models import Product,Category,Size,Subcategory,ProductColor,Color,ProductVariant
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import *
from cart.models import *
from order.models import *
from django.db.models import Q
from order.forms import *
from .forms import *
# Create your views here.


# store homepage display
def homepage(request):
   product = Product.objects.all()
   sub = Subcategory.objects.all()
   return render(request,'store_templates/homepage.html',{'product':product,'sub':sub})




# search products in search bar
def search_product(request):
    product = None
    if request.method == 'POST':
        print("search products")
        query = request.POST['query']
        product = Product.objects.filter(Q(name__icontains=query))
    return render(request, "store_templates\product_search.html", {'product':product})



# menscollection html rendering
def menscollection(request):
   product = Product.objects.filter(category_id=1)
   sub = Subcategory.objects.all()
   price_filter_form = PriceFilterForm(request.GET or None)

   if price_filter_form.is_valid():
        min_price = price_filter_form.cleaned_data['min_price']
        max_price = price_filter_form.cleaned_data['max_price']
        product = [product for product in product if any(variant.price >= min_price and variant.price <= max_price for variant in product.productvariant.all())]

       

   return render(request,'store_templates\menscollection.html',{'product':product,'sub':sub,'price_filter_form':price_filter_form})


# womencollection html rendering
def womencollection(request):
   product = Product.objects.filter(category_id=2)
   sub = Subcategory.objects.all()
   return render(request,'store_templates\womencollection.html',{'product':product,'sub':sub})


# product individual page 
def product_details(request,id):
  product = Product.objects.get(id=id)  
  flag = 1  
  sub = Subcategory.objects.all()
  v = product.productvariant.all()
  
 
  return render(request,'store_templates\product_details.html',{'product':product,'sub':sub})


# by sub category showing producst for user
def subcategory_filtering(request,id):
   sub = Subcategory.objects.all()
   sub_name = Subcategory.objects.get(pk=id).name
   product = Product.objects.filter(subcategory_id=id)

   return render(request,'store_templates\subcategory_filtering.html',{'product':product,'sub_name':sub_name,'sub':sub})



# check out page
def checkout_page(request):
    user=request.user
    flag = 0
    cart = Cart.objects.get(user=user)
    if cart.coupon:
       total_price = cart.coupon_total
    else:
       total_price = cart.cart_total

    total_quantity = cart.get_total_products()
    address = user.addresses.all()
    print(address)
    default_address = address
    if address:
        address_added = True
        for address in address:
           if address.status:
              print(address)
              default_address = address
    else:
        address_added = False
   
   # check if wallet payment avilable or not
    wallet = Wallet.objects.get(user=request.user)
    print(wallet)
    if wallet.wallet_amount >= total_price:
       flag = 1
       
    context = {
        
        'address_added': address_added,
        'default_address':default_address,
        'total_price':total_price,
         'total_quantity':total_quantity,
          'sub': Subcategory.objects.all(),
          'flag':flag

    }

   
    return render(request,'store_templates\checkout.html',context)



# myorders template
def myorders(request):
   orders = Order.objects.filter(user=request.user)
   print(orders)
   reason_form = CancelOrderForm()
   context ={
      'orders':orders,
      'reason_form':reason_form
   }
   
   return render(request,'store_templates\myorders.html',context)


# myorders  products template
def myorders_products(request,id):
   order = Order.objects.get(pk=id)
   orders = OrderItem.objects.filter(order=order)
   
   context ={
      'orders':orders,
      
   }
   
   return render(request,'store_templates\myorders_products.html',context)



# add to wishlist of a user
def addToWishlist(request,id):
   product = Product.objects.get(pk=id)
   print("selected product---",product)
   current_user = request.user
   try:
      if Wishlist.objects.get(product=product) is not None:
          print("already in wishlist")
   except:
      wishlist = Wishlist.objects.create(user=current_user,product=product)
      print(wishlist)

   return redirect('/')



# wishlist html rendering
def user_wishlist(request):
   current_user = request.user
   flag = True
   if current_user in CustomUser.objects.all():
      print(current_user)
      user_wishlist = Wishlist.objects.filter(user=current_user)
      print(user_wishlist)
      if user_wishlist.exists() is False:
         flag = False
         
      context = {
         'user_wishlist':user_wishlist,
         'flag':flag,
      }
      return render(request,'store_templates\wishlist.html',context)
   
   return redirect('signin')


# remove from wishlist
def remove_from_wishlist(request,id):
   current_user = request.user
   product = Product.objects.get(pk=id)
   if current_user in CustomUser.objects.all():
      product_in_wishlist = Wishlist.objects.get(user=current_user,product=product)
      product_in_wishlist.delete()
      
   return render(request,'store_templates/wishlist.html')



 
   # user wallet
def user_wallet(request):
   try:
      wallet = Wallet.objects.get(user=request.user)
      if wallet:
         print(wallet.wallet_amount)
   except:
       wallet = Wallet.objects.create(user=request.user,wallet_amount=0)
   return render(request,'store_templates/user_wallet.html',{'wallet':wallet})





#  user rewards section
def rewards(request):
   try:
      rewards = Rewards.objects.get(user=request.user)
   except:
      rewards = Rewards.objects.create(user=request.user,cashback_amount=0)
   context = {
              'rewards':rewards
       }
   return render(request,'store_templates/rewards.html',context)