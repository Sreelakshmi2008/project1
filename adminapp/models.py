from django.db import models


# category of prodcut
class Category(models.Model):
    name = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name


# sub category of prodcut
class Subcategory(models.Model):
    name = models.CharField(max_length=255,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    

# required sizes
class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# required colors model
class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


# product model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    # image = models.ImageField(upload_to='product_images/')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}-{self.subcategory.name}"


# product size variant with price
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="productvariant")
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    # color = models.ForeignKey(Color, on_delete=models.CASCADE)
    # color_image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=8, decimal_places=2)
  
    def __str__(self):
        return f"{self.product.name} - Size: {self.size.name}"


# product color variant with image
class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="productcolor")
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    color_image = models.ImageField(upload_to='product_images/') 
    

    def __str__(self):
        return f"{self.product.name} -  Color: {self.color.name}"