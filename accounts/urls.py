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



# forgot password and reset it
path('forgotPassword',views.forgotPassword,name='forgotPassword'),
path('forgotPassword_otp',views.forgotPassword_otp,name='forgotPassword_otp'),
path('resetPassword',views.resetPassword,name='resetPassword'),



# userprofile for user and add address
path('add_address',views.add_address,name='add_address'),
path('userprofile',views.userprofile,name='userprofile'),
path('edit_address/<int:id>/',views.edit_address,name='edit_address'),
path('delete_address/<int:id>/',views.delete_address,name='delete_address'),

# edit user details
path('edit_user_details',views.edit_user_details,name='edit_user_details'),

] 
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



