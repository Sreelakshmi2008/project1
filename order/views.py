import decimal
from typing import Any
from django.views import View
from django.shortcuts import render, redirect
from .models import *
from mystore.models import *
from adminapp.models import *
from cart.models import *
from accounts.models import *
from payment.models import *
from django.http import JsonResponse
from .forms import *
from payment.views import *
from cart.views import *
import datetime
import json
from django.conf import Settings
from django.urls import reverse
from payment.views import *



class place_order(View):

        def dispatch(self, request, *args, **kwargs):
                # Declare and assign instance attributes
                
                self.flag = 0
                print("place")
                self.current_user = request.user
                print(self.current_user)

                self.cart = Cart.objects.get(user=self.current_user)
                self.cart_items = CartItem.objects.filter(user=self.current_user)
                self.cart_count = self.cart_items.count()
                
                if self.cart.coupon:
                   self.total_price = self.cart.coupon_total
                else:
                  self.total_price = self.cart.get_total_price()
               
                      
                print(self.total_price)
                self.default_address_id = None
                # Call the default dispatch method
                return super().dispatch(request, *args, **kwargs)
                        
                
            
        def get(self,request):
            
            
          # if cart count is less than or equal to zero redirect back to homepage
            if self.cart_count <= 0:
                    return redirect('homepage')
            else:
               
                        data = Order()

                        
                        data.user = self.current_user
                        selected_option = request.GET.get('selectedOption')
                        payment_method_mapping = {
                                        'option1': 'COD',
                                        'option2': 'Razorpay',
                                        # Add more mappings as needed
                                }
                        print(selected_option)
                        payment_method_selected = payment_method_mapping.get(selected_option)
                        print(payment_method_selected)
                        if selected_option == 'option1':
                                print("first one")
                                payment_method = Payment.objects.create(user=self.current_user,payment_method='cod',amount_paid=self.total_price,status=False)
                                
                                data.payment = payment_method
                                
                                self.default_address_id = request.GET.get('defaultAddressId')
                                print(self.default_address_id)
                                data.shipping_address =  UserProfile.objects.get(id=self.default_address_id)
                                print(data.shipping_address)
                                data.order_total = self.total_price
                                print(data.user,data.payment,data.shipping_address,data.order_total)
                                data.save()
                                print(data)
                                # generate order number
                                yr = int(datetime.date.today().strftime('%Y'))
                                dt = int(datetime.date.today().strftime('%d'))
                                mt = int(datetime.date.today().strftime('%m'))
                                d = datetime.date(yr,mt,dt)
                                current_date = d.strftime("%Y%m%d")
                                order_number= current_date + str(data.id)
                                data.order_number = order_number
                                print(data.order_number,current_date)
                                data.save()
                                for item in self.cart_items:
                                        order = OrderItem.objects.create(user=request.user,
                                                product=item.product,
                                                product_variant=item.product_variant,
                                                product_color=item.product_color,
                                                order=data,
                                                quantity=item.quantity,
                                                ordered=True)
                                        print(order)
                                        print(item.product_variant.pdt_stock)
                                        p = item.product_variant
                                        p.pdt_stock -= item.quantity
                                        print(item.product_variant.pdt_stock)
                                        p.save()
                                        item.delete()
                                        
                                self.cart.coupon = None
                                flag = 1
                                self.cart.save()
                                
                                return JsonResponse({'message': 'Order placed successfully.','flag':flag,'id':order_number,'amount':self.total_price})
                        elif selected_option == 'option2':
                                    print("elif")
                                    o = order_payment(self.total_price)
                                    order_id = o['order_id']
                                    razorpay_order_total = o['total_price']
                                    print("back")
                                        

                                    payment_method = Payment.objects.create(user=self.current_user,payment_method=payment_method_selected,amount_paid=self.total_price,razorpay_order_id=order_id,status=False)
                                        
                                    data.payment = payment_method
                                        
                                    default_address_id = request.GET.get('defaultAddressId')
                                    data.shipping_address =  UserProfile.objects.get(id=default_address_id)
                                    print(data.shipping_address)
                                    data.order_total = self.total_price
                                    print(data.user,data.payment,data.shipping_address,data.order_total)
                                    data.save()
                                    print(data)
                                    # generate order number
                                    yr = int(datetime.date.today().strftime('%Y'))
                                    dt = int(datetime.date.today().strftime('%d'))
                                    mt = int(datetime.date.today().strftime('%m'))
                                    d = datetime.date(yr,mt,dt)
                                    current_date = d.strftime("%Y%m%d")
                                    order_number= current_date + str(data.id)
                                    data.order_number = order_number
                                    print(data.order_number,current_date)
                                    data.save()
                                    for item in self.cart_items:
                                        order = OrderItem.objects.create(user=request.user,
                                                product=item.product,
                                                product_variant=item.product_variant,
                                                product_color=item.product_color,
                                                order=data,
                                                quantity=item.quantity,
                                                ordered=True)
                                        print(order)
                                        item.delete()
                                        p = item.product_variant
                                        print(item.product_variant.pdt_stock)
                                        p.pdt_stock -= item.quantity
                                        print(item.product_variant.pdt_stock)
                                        p.save()
                                    
                                    self.cart.coupon = None
                                    self.cart.save()
                                    payment_id = payment_method.id
                                    redirect_url = reverse('razorpay_page') + f'?total={razorpay_order_total}&id={order_id}&order_number={order_number}&payment_id={payment_id}'
    
                                    return JsonResponse({'message': 'razorpay entered.','redirect':redirect_url})

class razorpay(place_order):
       def get(self,request):
              print(self.total_price)
             
              return render(request,'store_templates/razorpay.html')

       
                                        

def order_cancel(request,id):
       print("order cancel clicked ")
       order_to_cancel = Order.objects.get(pk=id)
       print(order_to_cancel)
       if request.method == "POST":
                
                reason_form = CancelOrderForm(request.POST)
                print("************************************************")
                print(reason_form)
                print("************************************************")
                if reason_form.is_valid():
                        
                        cancel_reason = reason_form.cleaned_data.get('cancel_reason')
                        print("reason is ---",cancel_reason,"status is -----",order_to_cancel.status,"payment method is------", order_to_cancel.payment.payment_method )
                        if order_to_cancel.payment.payment_method == 'cod':
                                order_to_cancel.status = 'Cancelled'
                                order_to_cancel.save()
                        elif order_to_cancel.payment.payment_method == 'Razorpay':
                                order_to_cancel.status = 'Cancelled'
                                order_to_cancel.save()
                                w = Wallet.objects.get(user=request.user)
                                w.wallet_amount = float(w.wallet_amount) + float(order_to_cancel.order_total)
                                print(w.wallet_amount)
                                w.save()
                                

                        print(order_to_cancel.status)
                        CancelOrder.objects.create(user=request.user,order=order_to_cancel,cancel_reason=cancel_reason)
                else:
                       print("not valid")
                        
       else:
              reason_select = "Select a reason"

       current_path = request.META['HTTP_REFERER']
       return redirect(current_path)
      

        
# order placing and payment using wallet
def wallet_pay(request):
          
        current_user = request.user
        wallet = Wallet.objects.get(user=current_user)
        cart = Cart.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(user=current_user)
        cart_count = cart_items.count()
        
        if cart.coupon:
                total_price = cart.coupon_total
        else:
                total_price = cart.get_total_price()         
            
          # if cart count is less than or equal to zero redirect back to homepage
        if cart_count <= 0:
                return redirect('homepage')
        else:        
               
                data = Order()

                data.user = current_user

                payment_method = Payment.objects.create(user=current_user,payment_method='Wallet',amount_paid=total_price,status=False)
                
                data.payment = payment_method
                
                default_address_id = request.GET.get('defaultAddressId')
                print(default_address_id)
                data.shipping_address =  UserProfile.objects.get(id=default_address_id)
                print(data.shipping_address)
                data.order_total = total_price
                print(data.user,data.payment,data.shipping_address,data.order_total)
                data.save()
                print(data)
                # generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d")
                order_number= current_date + str(data.id)
                data.order_number = order_number
                print(data.order_number,current_date)
                data.save()
                for item in cart_items:
                        order = OrderItem.objects.create(user=request.user,
                                product=item.product,
                                product_variant=item.product_variant,
                                product_color=item.product_color,
                                order=data,
                                quantity=item.quantity,
                                ordered=True)
                        print(order)
                        print(item.product_variant.pdt_stock)
                        p = item.product_variant
                        p.pdt_stock -= item.quantity
                        print(item.product_variant.pdt_stock)
                        p.save()
                        item.delete()
                        
                cart.coupon = None
                cart.save()
                wallet.wallet_amount = float(wallet.wallet_amount) - float(total_price)
                wallet.save()
                redirect_url = reverse('complete__wallet_payment') + f'?amount={total_price}&order_number={order_number}&payment_id={payment_method.id}'
                return JsonResponse({'message': 'Order placed successfully.','id':order_number,'amount':total_price,'redirect':redirect_url})
        




def return_order(request,id):
    print(id)
    if request.method=="POST":
        return_reason=request.POST.get('reason')
        try:
            order = get_object_or_404(Order, pk=id, user= request.user)
            order.status='Returned'
            order.return_reason = return_reason
            order.save()
            if order.payment.payment_method == 'Razorpay' or 'COD' or 'Wallet':
                wallet= Wallet.objects.get(user=request.user)
                refund_amount = decimal.Decimal(order.order_total)
                print(refund_amount)
                wallet.wallet_amount += refund_amount
                wallet.save()

        except Order.DoesNotExist:
            pass
    return redirect('myorders')