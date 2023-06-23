from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
   
# user signup and signin using password 
path('signup',views.signup,name='signup'),
path('signin',views.signin,name='signin'),

# sending and verifying otp 
path('otp_login',views.otp_login,name='otp_login'),
path('verifyotp',views.verify_otp,name='verifyotp'),


# signout from user account
path('signout',views.signout,name='signout'),


# userprofile for user and add address

path('add_address',views.add_address,name='add_address'),
path('userprofile',views.userprofile,name='userprofile'),
path('edit_address',views.edit_address,name='edit_address'),
path('delete_address',views.delete_address,name='delete_address'),



] 
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



