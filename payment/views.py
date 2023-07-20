from django.shortcuts import render,HttpResponse
from adminapp.models import *
from cart.models import *
from accounts.models import *
from order.models import *
import razorpay
from django.conf import settings
from .forms import razorpayForm
import json
from django.http import JsonResponse
# Create your views here.



# razorpay client creating function
def order_payment(amount):      
                client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
                
                razorpay_order = client.order.create(
                        {"amount": int(amount)*100, "currency": "INR", "payment_capture": "1"}
                    )
                
                print(razorpay_order," -----done--------")
                order_id = razorpay_order['id']
                
                
                context = {
                                                'order_id': razorpay_order['id'],
                                                'amount': razorpay_order['amount'],
                                                'razorpay_key': settings.RAZORPAY_KEY_ID,
                                                'total_price':amount,
                                                'razorpay_order':razorpay_order
                                               
                                            }
                return context


# razorpay pay button page
def razorpay_page(request):
        
        total = request.GET.get('total')
        id = request.GET.get('id')
        print(id)
        # Your code logic using the received parameters

        context = {

                'total': total,
                'id':id
        }
        return render(request,'store_templates/razorpay.html',context)


# razorpayment completed succesfully page
def complete_payment(request):
        amount = request.GET.get('amount')
        id= request.GET.get('id')
        user_payment = Payment.objects.get(user=request.user,payment_method='Razorpay',amount_paid=amount,razorpay_order_id=id)
        user_payment.status = True
        user_payment.save()
        context ={
                'id':id,
                'razorpay_payment_id' : request.GET.get('razorpay_payment_id'),
                'amount':amount
        }
        return render(request,'store_templates/complete_payment.html',context)






def user_payment_details_page(requset,id):
        user_payment_details = Payment.objects.get(id=id)

        order = Order.objects.get(payment_id=id)
        print(order)
        context = {
                'user_payment_details':user_payment_details,
                'order':order
        }
        return render(requset,'admin_templates/user_payment_details_page.html',context)


# apply coupon fun
def apply_coupon(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'GET':
        print('Coupon starts')
        data = {}
        
        coupon_code = request.GET.get('coupon')
        total_price = float(request.GET.get('totalPrice'))
        print(coupon_code,total_price)
        coupon = None
        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code)
            
            print(coupon)
                 
        except:
            print("not exist")
            data['message'] = 'Not a Valid Coupon'
            data['total'] = total_price
        if coupon:
            if  cart.coupon:
                
                data['message'] = 'Coupon Already Applied'
                print("already applied")
            else:
                minimum_amount = coupon.minimum_amount
                discount_price = coupon.discount_price
                if total_price >= minimum_amount:
                    total_price -= discount_price
                    cart.coupon_total = total_price
                    cart.coupon = coupon
                    cart.save()
                    data['message'] = f'{coupon.coupon_code} Applied'
                else:
                    data['message'] = 'Mininmum Amount Should be ',minimum_amount
            data['total'] = total_price
             
      

        return JsonResponse(data)
    return render(request,'store_templates/cart.html')



def complete__wallet_payment(request):
        amount = request.GET.get('amount')
        id= request.GET.get('payment_id')
        order_number= request.GET.get('order_number')
        user_payment = Payment.objects.get(pk=id,user=request.user,payment_method='Wallet',amount_paid=amount)
        user_payment.status = True
        user_payment.save()
        context ={
                'id':order_number,
                'razorpay_payment_id' : id,
                'amount':amount
        }
        return render(request,'store_templates/complete_payment.html',context)
