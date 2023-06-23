from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
path('',views.homepage,name='homepage'),
path('menscollection',views.menscollection,name='menscollection'),
path('womencollection',views.womencollection,name='womencollection'),
path('product_details/<int:id>/',views.product_details,name='product_details'),
path('subcategory_filtering/<int:id>/',views.subcategory_filtering,name='subcategory_filtering'),


# checkout
path('checkout_page',views.checkout_page,name='checkout_page'),
path('order_summary',views.order_summary,name='order_summary'),


            

]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

