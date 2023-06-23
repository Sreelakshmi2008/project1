from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path('cart',views.cart,name="cart"),

path('add_to_cart',views.add_to_cart,name="add_to_cart"),

path('delete_cart_item/<int:id>/',views.delete_cart_item,name="delete_cart_item"),

# path('cart_item_search',views.cart_item_search,name="cart_item_search"),
            

]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

