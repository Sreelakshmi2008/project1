from django.urls import path
from . import views

urlpatterns = [

path('place_order',views.place_order.as_view(),name="place_order"),


# confirm order
path('razorpay',views.razorpay.as_view(),name="razorpay"),

# order cancel by user
path('order_cancel/<int:id>',views.order_cancel,name="order_cancel"),


path('wallet_pay',views.wallet_pay,name="wallet_pay"),

]