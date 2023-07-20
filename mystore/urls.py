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
path('search_product',views.search_product,name="search_product"),
path('addToWishlist/<int:id>',views.addToWishlist,name="addToWishlist"),
path('user_wishlist',views.user_wishlist,name="user_wishlist"),
path('remove_from_wishlist/<int:id>',views.remove_from_wishlist,name="remove_from_wishlist"),



# checkout
path('checkout_page',views.checkout_page,name='checkout_page'),


# myorders url
path('myorders',views.myorders,name='myorders'),
path('myorders_products/<int:id>',views.myorders_products,name='myorders_products'),


path('user_wallet',views.user_wallet,name='user_wallet'),
path('rewards',views.rewards,name='rewards'),
            

]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

