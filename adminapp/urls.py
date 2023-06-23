from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   
  
# admin login and admin logout
path('adminlogin',views.admin_login.as_view(),name='adminlogin'),
path('adminlogout',views.admin_logout,name='adminlogout'),
path('adminpanel',views.adminpanel,name='adminpanel'),


# admin accounts section urls
path('admin_accounts',views.admin_accounts,name='admin_accounts'),
path('user_search',views.user_search,name='user_search'),
path('block_user/<int:id>/',views.block_user,name='block_user'),
path('unblock_user/<int:id>/',views.unblock_user,name='unblock_user'),


# admin products section
path('products',views.products,name='products'),

path('add_products',views.add_products,name='add_products'),

path('add_product_variant/<int:id>/',views.add_product_variant,name='add_product_variant'),
path('add_product_color/<int:id>/',views.add_product_color,name='add_product_color'),

path('add_color_options',views.add_color_options,name='add_color_options'),

path('edit_product',views.edit_product,name= 'edit_product'),
path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
path('productbysubcategories/<int:id>/',views.productbysubcategories,name='productbysubcategories'),
path('productbycategories/<int:id>/',views.productbycategories,name='productbycategories'),
path('add_subcategory',views.add_subcategory,name='add_subcategory'),
path('add_category',views.add_category,name='add_category'),
path('delete_subcategory/<int:id>/',views.delete_subcategory,name='delete_subcategory'),
path('delete_category/<int:id>/',views.delete_category,name='delete_category'),



# admin side cart 
path('admin_cart',views.admin_cart,name="admin_cart"),
] 
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



