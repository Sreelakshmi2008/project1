from django import forms
from .models import ProductVariant,Category,Size,Subcategory,Product,Color,ProductColor



# category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# sub category form
class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']

# size input  form
class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['name']

# color input form
class ColorForm(forms.ModelForm):
    class Meta:
        model = Color
        fields = ['name']



# product form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category','subcategory','name','description']



# product size variant form
class ProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['product','size','price','pdt_stock']


# product color variant form
class ProductColorForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = ['product','color', 'color_image']
        
