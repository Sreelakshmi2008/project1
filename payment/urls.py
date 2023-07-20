from django.urls import path
from . import views

urlpatterns = [
path('order_payment',views.order_payment,name="order_payment"),

path('razorpay_page',views.razorpay_page,name="razorpay_page"),

path('complete_payment',views.complete_payment,name="complete_payment"),
path('complete__wallet_payment',views.complete__wallet_payment,name="complete__wallet_payment"),

path('user_payment_details_page/<int:id>/',views.user_payment_details_page,name="user_payment_details_page"),

path('apply_coupon',views.apply_coupon,name="apply_coupon"),



    # Other URL patterns


      # first buy copon
]