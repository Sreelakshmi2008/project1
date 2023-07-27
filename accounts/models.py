from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self,email,password=None, **extra_fields):

        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email,password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,password, **extra_fields)

    def create_superuser(self, email,password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,password, **extra_fields)


# custom user model for user accounts
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True,null=True)
    name = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(unique=True,max_length=15,null=True)
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def set_password(self, raw_password):
        # Hash and set the password
        self.password = make_password(raw_password)

   

   

class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='addresses')
    address_line_1 = models.CharField(blank=True,max_length=100)
    address_line_2 = models.CharField(blank=True,max_length=100)
    city = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)
    pincode = models.IntegerField(null=True)
    status = models. BooleanField(default=False)


    def __str__(self):
        return f"{self.user.name}-{self.address_line_1}"
    
    def full_address(self):
        return f"{self.address_line_1} , {self.address_line_2} , {self.city} , {self.state} - {self.pincode} "
    


@receiver(pre_save, sender=UserProfile)
def restrict_status(sender, instance, **kwargs):
        if instance.status:
            UserProfile.objects.exclude(id=instance.id).update(status=False)