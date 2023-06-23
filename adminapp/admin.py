from django.contrib import admin
from .models import Product,Category,Subcategory,Size,Color,ProductVariant,ProductColor
# Register your models here.


admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(ProductColor)
admin.site.register(Color)
admin.site.register(ProductVariant)
