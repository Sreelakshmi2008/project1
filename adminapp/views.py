from django.views import View
from django.contrib import messages,auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from django.db.models import Q
from .models import Product,Category,Subcategory,Size,Color,ProductVariant
from .forms import ProductForm,CategoryForm,SubcategoryForm,SizeForm,ColorForm,ProductVariantForm,ProductColorForm
from cart.models import Cart,CartItem
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

def adminpanel(request):
    return render(request, 'admin_templates/adminpanel.html')





# ADMIN USER ACCOUNTS SECTION


# user accounts display in admin side
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



# add product from admin side
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
def add_product_variant(request,id):
         product = Product.objects.get(id=id)
         fm= ProductVariantForm()
         print("yes")
         if request.method == 'POST':
            fm = ProductVariantForm(request.POST,request.FILES)
            if fm.is_valid():
                print("valid")
                fm.save()  
                print('success')
                return redirect('products')
         else:
             fm=ProductVariantForm()
                   
         context = {
            
            'fm':fm,
            'productid':id,
            'name':product.name
        
         }
         return render(request,'admin_templates/add_product_variant.html',context)



# add product color using ProductColor model
def add_product_color(request,id):
         product = Product.objects.get(id=id)
         fm= ProductColorForm()
         print("yes")
         if request.method == 'POST':
            fm = ProductColorForm(request.POST,request.FILES)
            if fm.is_valid():
                print("valid")
                fm.save()  
                print('success')
                return redirect('products')
         else:
             fm=ProductColorForm()
                   
         context = {
            'product':product,
            'fm':fm
         }
         return render(request,'admin_templates/add_product_color.html',context)
    


# add color options 
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
def delete_subcategory(request,id):
        pi = Subcategory.objects.get(pk=id)
        pi.delete()
        return redirect('products')


# delete subcategory
def delete_category(request,id):
        pi = Category.objects.get(pk=id)
        pi.delete()
        return redirect('products')


# delete product
def delete_product(request, id):
        pi = Product.objects.get(pk=id)
        pi.delete()
        return redirect('products')


# edit product
def edit_product(request):
     
     return render(request,'admin_templates/edit-product.html')


# filter products by sub category in admin side
def productbysubcategories(request,id):
        pdt = Product.objects.filter(subcategory_id=id)
        return render(request,"admin_templates/subcategories.html",{'pdt':pdt})


# filte products by category in adminside
def productbycategories(request,id):
        pdt = Product.objects.filter(category_id=id)
        return render(request,"admin_templates/categories.html",{'pdt':pdt})





# ADMIN SIDE CART SECTION

# admin side cart display
def admin_cart(request):
     cart = Cart.objects.all()
     cartitems = Cart.objects.all()
     return render(request,'admin_templates/admin_cart.html',{'cart':cart,'cartitems':cartitems})