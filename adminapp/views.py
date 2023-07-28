from django.views import View
from django.contrib import messages,auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import *
from django.db.models import Q,Count,Value as V,CharField
from .models import *
from .forms import *
from cart.models import *
from order.models import *
from payment.forms import *
from django.db.models.functions import ExtractMonth,ExtractDay,Concat
# Create your views here.


# admin login into adminpanel
class admin_login(View):
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email,password=password)
        if  user.is_superuser:
            login(request,user)
            return redirect('adminpanel')
        else:
            messages.error(request,"Bad credentials")
            return redirect('adminlogin')
    def get(self,request):
       return render(request, 'admin_templates/adminlogin.html')



# admin logout from adminpanel
def admin_logout(request):
    logout(request)
    messages.success(request,"Logged out succesfully")
    return redirect('adminlogin')



#adminpanel html rendering
import calendar
@login_required(login_url='adminlogin')
def adminpanel(request):
    delivered_orders = Order.objects.filter(status='Delivered')
    delivered_orders = Order.objects.filter(status='Delivered')
    delivered_orders_by_months = delivered_orders.annotate(delivered_month=ExtractMonth('created_at')).values('delivered_month').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_count')
    print( delivered_orders_by_months)
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
         delivered_orders_month.append(calendar.month_name[d['delivered_month']])
         delivered_orders_number.append(list(d.values())[1])


    order_by_day = Order.objects.annotate(month=ExtractMonth('created_at'),day=ExtractDay('created_at')).values('month','day').annotate(count=Count('id')).values('month', 'day', 'count').annotate(date=Concat('month', V('/'), 'day', output_field=CharField()))
    
    monthNumber = []
    totalOrders = []
    dayNumber = []
    for o in order_by_day:
        month_name = calendar.month_name[o['month']]
        day_number = o['day']
        monthNumber.append(f"{month_name} {day_number}")
        dayNumber.append(day_number)
        totalOrders.append(o['count'])
    print(delivered_orders_number)
    
    context ={
         'delivered_orders':delivered_orders,
         'order_by_months':order_by_day,
         'monthNumber':monthNumber,
         'totalOrders':totalOrders,
         'delivered_orders_number':delivered_orders_number,
         'delivered_orders_month':delivered_orders_month,
         'delivered_orders_by_months':delivered_orders_by_months,


    }
    return render(request, 'admin_templates/adminpanel.html',context)





# ADMIN USER ACCOUNTS SECTION


# user accounts display in admin side
@login_required(login_url='adminlogin')
def admin_accounts(request):
    stu = CustomUser.objects.all()
    return render(request,'admin_templates/admin_accounts.html',{'stu':stu})


# user accounts search in admin side
def user_search(request):
    if request.method == 'POST':
        query = request.POST['query']
        user = CustomUser.objects.filter(Q(email__icontains=query) | Q(id__contains=query))

    return render(request,"admin_templates/user_search.html",{'user': user})

# block user from admin side
def block_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
        return redirect('admin_accounts')

# unblock user froom admin side
def unblock_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        return redirect('admin_accounts')



#  ADMIN PRODUCT SECTION


# products list display in admin side
@login_required(login_url='adminlogin')
def products(request):
    product = Product.objects.all()
    subcategories = Subcategory.objects.all()
    categories = Category.objects.all()
    variants = ProductVariant.objects.all()
    context = {
         'product':product,
         'subcategories':subcategories,
         'categories':categories,
         'variants':variants
    }
    return render(request,'admin_templates/products.html',context)



# product variant of each product
@login_required(login_url='adminlogin')
def variant_by_product(request,id):
      product = Product.objects.get(pk=id)
      
      context = {
         'product':product,
        
      }
      return render(request,'admin_templates/product_variants.html',context)




# product color of each product
@login_required(login_url='adminlogin')
def color_of_product(request,id):
      product = Product.objects.get(pk=id)
      
      context = {
         'product':product,
        
      }
      return render(request,'admin_templates/product_colors.html',context)



# products  search in admin side

def product_search(request):
    if request.method == 'POST':
        query = request.POST['query']
        p = Product.objects.filter(Q(name__icontains=query) | Q(id__contains=query))

    return render(request,"admin_templates/product_search.html",{'product': p})



# add product from admin side
@login_required(login_url='adminlogin')
def add_products(request):
       fm= ProductForm()
       if request.method == "POST":
            fm= ProductForm(request.POST,request.FILES)
            if fm.is_valid():
                fm.save()  
                print('success')
                return redirect('products')
            else:
                 fm=ProductForm()
            
            return redirect('products')
       context = {
                       "fm":fm,
                       }
       return render(request,'admin_templates/add_products.html',context)



# add product size,price using ProductVariant model
@login_required(login_url='adminlogin')
def add_product_variant(request,id):
         product = Product.objects.get(id=id)
         fm= ProductVariantForm()
         print("yes")
         if request.method == 'POST':
            fm = ProductVariantForm(request.POST,request.FILES)
            product_sizes = product.productvariant.all()
            if fm.is_valid():
                print("size")
                fm.save()  
                print('success')
                redirect('products')
         else:
             fm=ProductVariantForm()
                   
         context = {
            
            'fm':fm,
            'productid':id,
            'name':product.name
        
         }
         return render(request,'admin_templates/add_product_variant.html',context)



# edit pdt variant of each pdt
def edit_pdt_variant(request,id):
     p = ProductVariant.objects.get(pk=id)
     fm= ProductVariantForm(instance=p)
     if request.method == 'POST':
            fm = ProductVariantForm(request.POST,instance=p)
            if fm.is_valid():
               
                fm.save()  
                print('success')
                redirect('products')
     else:
             fm=ProductVariantForm(instance=p)

     context = {
            
            'fm':fm,
            'productid':id,
         }
     return render(request,'admin_templates/add_product_variant.html',context)



# product variant delete
def delete_pdt_variant(request,id):
    p = ProductVariant.objects.filter(pk=id)
    print(p)
    p.delete()
    return redirect('products')


# add product color using ProductColor model
@login_required(login_url='adminlogin')
def add_product_color(request,id):
         product = Product.objects.get(id=id)
         fm= ProductColorForm()
         print("yes")
         if request.method == 'POST':
            fm = ProductColorForm(request.POST,request.FILES)
            if fm.is_valid():
                print("valid")
                fm.save()  
                print('success',ProductColorForm(request.POST,request.FILES))
                redirect('products')
         else:
             fm=ProductColorForm()
                   
         context = {
            'product':product,
            'fm':fm
         }
         return render(request,'admin_templates/add_product_color.html',context)


# product color delete for each pdt
def delete_pdt_color(request,id):
    p = ProductColor.objects.get(pk=id)
    print(p)
    p.delete()
    return redirect('products')


# add color options 
@login_required(login_url='adminlogin')
def add_color_options(request):
       
         fm= ColorForm()
         print("yes")
         if request.method == 'POST':
            fm = ColorForm(request.POST)
            if fm.is_valid():
                print("valid")
                fm.save()  
                print('success')
                return redirect('products')
         else:
             fm=ColorForm()
                   
         context = {
            
            'fm':fm
         }
         return render(request,'admin_templates/add_product_color.html',context)



# add sub category for product
@login_required(login_url='adminlogin')
def add_subcategory(request):
    fm = SubcategoryForm()
    if request.method == 'POST':
        fm = SubcategoryForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('products')
    else:
        fm = SubcategoryForm()
    return render(request,'admin_templates/add_subcategory.html',{'fm':fm})



# add category for product
@login_required(login_url='adminlogin')
def add_category(request):
    fm = CategoryForm()
    if request.method == 'POST':
        fm = CategoryForm(request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('products')
    else:
        fm = CategoryForm()
    return render(request,'admin_templates/add_category.html',{'fm':fm})


# delete category
@login_required(login_url='adminlogin')
def delete_subcategory(request,id):
        pi = Subcategory.objects.get(pk=id)
        pi.delete()
        return redirect('products')


# delete subcategory
@login_required(login_url='adminlogin')
def delete_category(request,id):
        pi = Category.objects.get(pk=id)
        pi.delete()
        return redirect('products')


# delete product
@login_required(login_url='adminlogin')
def delete_product(request, id):
        pi = Product.objects.get(pk=id)
        pi.delete()
        return redirect('products')


# edit product
@login_required(login_url='adminlogin')
def edit_product(request,id):
     edit_product = Product.objects.get(id=id)
     
     fm = ProductForm(instance=edit_product)
     if request.method == 'POST':
        fm = ProductForm(request.POST,instance=edit_product)
        
        if fm.is_valid():
            fm.save()
            redirect('products')
        else:
            edit_product = Product.objects.get(id=id)
        
            fm = ProductForm(instance=edit_product)
     return render(request,'admin_templates/edit-product.html',{'fm':fm,'edit_product':edit_product})



 
       
# filter products by sub category in admin side
@login_required(login_url='adminlogin')
def productbysubcategories(request,id):
        pdt = Product.objects.filter(subcategory_id=id)
        return render(request,"admin_templates/subcategories.html",{'pdt':pdt})


# filte products by category in adminside
@login_required(login_url='adminlogin')
def productbycategories(request,id):
        pdt = Product.objects.filter(category_id=id)
        return render(request,"admin_templates/categories.html",{'pdt':pdt})





# ADMIN SIDE CART SECTION

# admin side cart display
@login_required(login_url='adminlogin')
def admin_cart(request):
     cart = Cart.objects.all()
     
     return render(request,'admin_templates/admin_cart.html',{'cart':cart})


# cart items by user
@login_required(login_url='adminlogin')
def admin_cart_by_user(request,id):
     cart = Cart.objects.get(pk=id)
     cartitems = CartItem.objects.filter(cart=cart)
     return render(request,'admin_templates/admin_cart_by_user.html',{'cart':cart,'cartitems':cartitems})
     




# cart  search in admin side
def cart_search(request):
    if request.method == 'POST':
        query = request.POST['query']
        p = Cart.objects.filter(Q(id__contains=query))
        u = CustomUser.objects.filter(email__icontains=query)
        if u:
             for u in u:
                  p = Cart.objects.filter(user=u)
        context = {
             'cart':p,
             
        }
    return render(request,"admin_templates/cart_search.html",{'cart': p})


# ADMIN SIDE ORDERS SECTION


# admin side order display
@login_required(login_url='adminlogin')
def admin_order(request):
     order = Order.objects.all().order_by("-created_at")
     
     return render(request,'admin_templates/admin_orders.html',{'order':order})



# edit order status by admin
@login_required(login_url='adminlogin')
def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
            order = Order.objects.get(pk=id)
            order.status = status
            order.save()
        except Order.DoesNotExist:
            pass
    return redirect("admin_order")



# order items display by each order
@login_required(login_url='adminlogin')
def admin_order_by_user(request,id):
      order = Order.objects.get(pk=id)
      user_orders = OrderItem.objects.filter(order=order)
      return render(request,'admin_templates/admin_order_by_user.html',{'user_orders':user_orders,'order':order})
     


# order  search in admin side
def order_search(request):
    if request.method == 'POST':
        query = request.POST['query']
        p = Order.objects.filter(Q(id__contains=query) | Q(order_number__icontains=query))
    
        print(p)
        context = {
             'order':p,
             

        }
    return render(request,"admin_templates/order_search.html",context)


# ADMIN COUPON MANAGEMENT


# coupons listing
@login_required(login_url='adminlogin')
def admin_coupons(request):
     coupons = Coupon.objects.all()
     context ={
          'coupons':coupons
     }
     return render(request,'admin_templates/admin_coupons.html',context)



# add coupon 
@login_required(login_url='adminlogin')
def add_coupon(request):
       
     fm = couponForm()
     if request.method == "POST":
          fm = couponForm(request.POST)
          if fm.is_valid():
               print("coupon form valid")
               fm.save()
               redirect('admin_coupons')
     
          else:
             fm = couponForm()
     
     context = {
         
          'fm':fm
     }

     return render(request,'admin_templates/add_coupon.html',context)



# edit existing coupons
@login_required(login_url='adminlogin')
def admin_coupon_edit(request,id):
     
     coupon = Coupon.objects.get(pk=id)
     print(coupon)
     fm = couponForm(instance=coupon)
     print(fm)
     if request.method == "POST":
          fm = couponForm(request.POST,instance=coupon)
          if fm.is_valid():
               print("coupon form valid")
               fm.save()
               redirect('admin_coupons')
     
          else:
             fm = couponForm(instance=coupon)
     
     context = {
          'coupon':coupon,
          'fm':fm
     }

     return render(request,'admin_templates/coupon_edit.html',context)



# delete coupon from admin side
def delete_coupon(request,id):
     coupon_to_delete = Coupon.objects.get(pk=id)
     coupon_to_delete.delete()
     
     return redirect('admin_coupons')



# wallets listing
@login_required(login_url='adminlogin')
def admin_wallet(request):
     wallets = Wallet.objects.all()
     context ={
          'wallets':wallets
     }
     return render(request,'admin_templates/admin_wallet.html',context)



# rewards listing
@login_required(login_url='adminlogin')
def admin_reward(request):
     rewards = Rewards.objects.all()
     context ={
          'rewards':rewards
     }
     return render(request,'admin_templates/admin_reward.html',context)