from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart,CartItem
from accounts.models import CustomUser
from adminapp.models import Product,Category,Size,Subcategory,ProductVariant,Color,ProductColor
import json
from django.http import JsonResponse
from django.db.models import Q
from payment.models import *
from django.contrib import messages
from payment.views import *
# Create your views here.


# add to cart function
def add_to_cart(request):  
        id = request.GET['productid']
        print(id)
        user = request.user if request.user.is_authenticated else None
        cart,_= Cart.objects.get_or_create(user=user)
        product =Product.objects.get(pk=id)      
        price = request.GET['selectedprice']
        size =request.GET['selectedsize']
        color = request.GET['selectedcolor']
        
        print(price)
        print(size)
        print(color)
        
       
        color_id = Color.objects.filter(name=color).values_list('pk', flat=True).first()
        print(color_id)
        product_color = ProductColor.objects.get(product_id=id,color_id=color_id)
        print(product_color)
        size_id = Size.objects.filter(name=size).values_list('pk', flat=True).first()
        print(size_id)
        product_variant = ProductVariant.objects.get(product_id=id,size_id=size_id)
        print(product_variant)
       
        if product_variant and product_color:
            try:
               if CartItem.objects.get(user=user,cart=cart,product=product,product_variant=product_variant,product_color=product_color):
                    cart_item = CartItem.objects.get(user=user,cart=cart,product=product,product_variant=product_variant,product_color=product_color)
                    print("there is an item")
                    cart_item.quantity = cart_item.quantity + 1
                    
                    cart_item.save()
                    c = cart_item.cart
                    print(c.coupon,"before")
                    c.coupon = None
                    print(c.coupon)
                    c.save()
               else:
                   raise Exception("no same item in cart")
            except Exception as e:
                error_message = f"Error occurred: {str(e)}"
                print(error_message)
                CartItem.objects.create(user=user,cart=cart,product=product,product_variant=product_variant,product_color=product_color,quantity=1)
                c = cart_item.cart
                print(c.coupon,"before")
                c.coupon = None
                print(c.coupon)
                c.save()
                
        return JsonResponse({'status':400,"message":"added"})




# delete item form cart
def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    
    cart_item.delete()
    c = cart_item.cart
    print(c.coupon,"before")
    c.coupon = None
    print(c.coupon)
    c.save()
    
    return redirect('cart')




# cart display to user
def cart(request):
    user = request.user if request.user.is_authenticated else None
    
    try:
        if user:
            
            cart,_ = Cart.objects.get_or_create(user=user)
            print(cart)
            cart_items = CartItem.objects.filter(user=user)
            if cart_items:
                    if cart.coupon:
                        print("there is coupon----",cart.coupon)
                    
                        sum = cart.coupon_total
                       
                    else:
                       sum = cart.get_total_price()
                       cart.cart_total = sum
                       cart.save()
                    total = cart.get_total_products()
                    print(total,sum)
                    context = {
                        'cart_items': cart_items,
                        'cart': cart,
                        'sum':sum,
                        'total':total,
                        'coupons':Coupon.objects.all()
                        
                    }
                    return render(request, 'store_templates/cart.html', context)
            else:
                message = "Your Cart is Empty"
                return render(request, 'store_templates/cart.html', {'message': message})
        else:
            raise Exception("User not authenticated")  # Raise an exception if the user is not authenticated
    except Exception as e:
        # Handle the exception appropriately
        # For example, you can log the error or display a user-friendly message
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        return redirect('homepage')
    # return render(request, 'store_templates\cart.html')





# update item quantity in cart function using ajax
def update_cart_item_quantity(request):
        print('entered')
        cart = Cart.objects.get(user=request.user)
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')
        
        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           print('try')
           cart_item = CartItem.objects.get(id=cart_item_id) 
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            print("increases")
            
            if cart_item.product_variant.pdt_stock > cart_item.quantity:
                cart_item.quantity += 1
                c = cart_item.cart
                print(c.coupon,"before")
                c.coupon = None
                print(c.coupon)
                c.save()
                print(cart_item.quantity)
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
            c = cart_item.cart
            print(c.coupon,"before")
            c.coupon = None
            print(c.coupon)
            c.save()
        cart_item.save()
        total_items = cart.get_total_products()
        return JsonResponse({'status': 200, 'quantity': cart_item.quantity,'total':cart.get_total_price(),'total_items':total_items})

# def cart_item_search(request):
#     if request.method == 'POST':
#         query = request.POST['query']
#         cartitems = CartItem.objects.filter(Q(user__icontains=query) | Q(product_size__contains=query) | Q(product_color__contains=query))

#     return render(request, "cart_item_search.html",{'cartitems':cartitems})








        

