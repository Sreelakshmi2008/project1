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
path('product_search',views.product_search,name='product_search'),
path('add_products',views.add_products,name='add_products'),

path('add_product_variant/<int:id>/',views.add_product_variant,name='add_product_variant'),
path('add_product_color/<int:id>/',views.add_product_color,name='add_product_color'),

path('add_color_options',views.add_color_options,name='add_color_options'),

path('edit_product/<int:id>/',views.edit_product,name= 'edit_product'),
path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
path('productbysubcategories/<int:id>/',views.productbysubcategories,name='productbysubcategories'),
path('productbycategories/<int:id>/',views.productbycategories,name='productbycategories'),
path('add_subcategory',views.add_subcategory,name='add_subcategory'),
path('add_category',views.add_category,name='add_category'),
path('delete_subcategory/<int:id>/',views.delete_subcategory,name='delete_subcategory'),
path('delete_category/<int:id>/',views.delete_category,name='delete_category'),



path('variant_by_product/<int:id>/',views.variant_by_product,name='variant_by_product'),
path('edit_pdt_variant/<int:id>/',views.edit_pdt_variant,name='edit_pdt_variant'),
path('delete_pdt_variant/<int:id>/',views.delete_pdt_variant,name='delete_pdt_variant'),


path('color_of_product/<int:id>/',views.color_of_product,name='color_of_product'),
path('delete_pdt_color/<int:id>/',views.delete_pdt_color,name='delete_pdt_color'),


# admin side cart 
path('admin_cart',views.admin_cart,name="admin_cart"),
path('admin_cart_by_user/<int:id>/',views.admin_cart_by_user,name="admin_cart_by_user"),
path('cart_search',views.cart_search,name="cart_search"),


# admin side orders list
path('admin_order',views.admin_order,name="admin_order"),
path('order_search',views.order_search,name="order_search"),
path('edit_order/<int:id>',views.edit_order,name="edit_order"),
path('admin_order_by_user/<int:id>',views.admin_order_by_user,name="admin_order_by_user"),

# adim side coupons list
path('admin_coupons',views.admin_coupons,name="admin_coupons"),
path('admin_coupon_edit\<int:id>',views.admin_coupon_edit,name="admin_coupon_edit"),
path('add_coupon',views.add_coupon,name="add_coupon"),
path('delete_coupon/<int:id>/',views.delete_coupon,name="delete_coupon"),



# admin side wallet and rewards
path('admin_wallet',views.admin_wallet,name="admin_wallet"),
path('admin_reward',views.admin_reward,name="admin_reward"),
] 
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



