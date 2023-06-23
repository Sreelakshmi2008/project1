from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart,CartItem
from accounts.models import CustomUser
from adminapp.models import Product,Category,Size,Subcategory,ProductVariant,Color,ProductColor
import json
from django.http import JsonResponse
from django.db.models import Q

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
        quantity =request.GET['selectedquantity']
        print(price)
        print(size)
        print(color)
        print(quantity)
        color_id = Color.objects.filter(name=color).values_list('pk', flat=True).first()
        print(color_id)
        product_color = ProductColor.objects.get(product_id=id,color_id=color_id)
        print(product_color)
        size_id = Size.objects.filter(name=size).values_list('pk', flat=True).first()
        print(size_id)
        product_variant = ProductVariant.objects.get(product_id=id,size_id=size_id)
        print(product_variant)
        product_color = ProductColor.objects.get(product_id=id,color_id=color_id)
        print(product_color)
        if product_variant and product_color:
            # cart_item,item_created = CartItem.objects.get_or_create(user=user,cart=cart,product=product)
            # if cart_item:
            #     print("there is an item")
            #     cart_item.quantity = cart_item.quantity + int(quantity)
            #     cart_item.save()
            # else:
            #     print("new item created")
            CartItem.objects.create(user=user,cart=cart,product=product,product_variant=product_variant,product_color=product_color,quantity=quantity)
    
        return JsonResponse({'status':400,"message":"added"})




# delete item form cart
def delete_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
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
                sum = cart.get_total_price()
                total = cart.get_total_products()
                context = {
                    'cart_items': cart_items,
                    'cart': cart,
                    'sum':sum,
                    'total':total
                }
                return render(request, 'store_templates\cart.html', context)
            else:
                message = "Your Cart is Empty"
                return render(request, 'store_templates\cart.html', {'message': message})
        else:
            raise Exception("User not authenticated")  # Raise an exception if the user is not authenticated
    except Exception as e:
        # Handle the exception appropriately
        # For example, you can log the error or display a user-friendly message
        error_message = f"Error occurred: {str(e)}"
        print(error_message)
        return redirect('homepage')
    return render(request, 'store_templates\cart.html')



# def cart_item_search(request):
#     if request.method == 'POST':
#         query = request.POST['query']
#         cartitems = CartItem.objects.filter(Q(user__icontains=query) | Q(product_size__contains=query) | Q(product_color__contains=query))

#     return render(request, "cart_item_search.html",{'cartitems':cartitems})








# def update_cart_item(request, id):
#    cart_item = get_object_or_404(CartItem, id=id)
#    if request.method == 'POST':
#         new_quantity = int(request.POST.get('quantity', 0))
#         if new_quantity >= 0:
#             cart_item.quantity = new_quantity
#             cart_item.save()
#    return redirect('cart:carts')


# def update_cart_item(request, id):
#     cart_item = get_object_or_404(CartItem, id=id)
#     if request.method == 'POST':
#         new_quantity = int(request.POST.get('quantity', 0))
#         if new_quantity >= 0:
#             cart_item.quantity = new_quantity
#             cart_item.save()

#     # Prepare the data to be sent back in the AJAX response
#     data = {
#         'subtotal': cart_item.get_subtotal(),
#     }

#     # Return the updated data as a JSON response
#     return JsonResponse(data)
