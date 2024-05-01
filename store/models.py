from django.db import models
from django.contrib.auth.models import User
import datetime
import os
# Create your models here.
def get_file_path(request, filename):
    original_filename=filename
    TimeNow=datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename= "%s%s" % (TimeNow, original_filename)
    return os.path.join('uploads/', filename)
class Category(models.Model):
    slug=models.CharField(max_length=150, null=False, blank=False)
    name=models.CharField(max_length=150, null=False, blank=False)
    image=models.ImageField(upload_to=get_file_path, null=True, blank=True)
    description=models.TextField(max_length=500, null=False, blank=False)
    status=models.BooleanField(default=False, help_text="0=default,1=Hidden")
    trending=models.BooleanField(default=False, help_text="0=default,1=Trending")
    meta_title=models.CharField(max_length=150,null=False, blank=False)
    meta_keywords=models.CharField(max_length=150,null=False, blank=False)
    meta_description=models.TextField(max_length=500, null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name    
    
class Product(models.Model):
        category=models.ForeignKey(Category,on_delete=models.CASCADE)
        slug=models.CharField(max_length=150, null=False, blank=False)
        name=models.CharField(max_length=150, null=False, blank=False)
        product_image=models.ImageField(upload_to=get_file_path, null=True, blank=True)
        small_description=models.CharField(max_length=250, null=False, blank=False)
        quantity=models.IntegerField(null=False, blank=False)
        description=models.TextField(max_length=500, null=False, blank=False)
        original_price=models.FloatField(null=False, blank=False)
        selling_price=models.FloatField(null=False, blank=False)
        status=models.BooleanField(default=False, help_text="0=default,1=Hidden")
        trending=models.BooleanField(default=False, help_text="0=default,1=Trending")
        tag=models.CharField(max_length=150,null=False, blank=False)
        meta_title=models.CharField(max_length=150,null=False, blank=False)
        meta_keywords=models.CharField(max_length=150,null=False, blank=False)
        meta_description=models.TextField(max_length=500, null=False, blank=False)
        created_at=models.DateTimeField(auto_now_add=True)
    
        def __str__(self):
            return self.name

class Cart(models.Model):
     user= models.ForeignKey(User, on_delete=models.CASCADE)
     product=models.ForeignKey(Product, on_delete=models.CASCADE)
     product_qty=models.IntegerField(null=False, blank=False)
     created_at=models.DateTimeField(auto_now_add=True)
     
     
  
# class Product_Review(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     product=models.ForeignKey(Product, on_delete=models.CASCADE)
#     review_text=models.TextField()
#     review_rating=models.IntegerField(default=0)
#     email=models.EmailField()
#     name = models.CharField(max_length=255)
    
#     def __str__(self):
#             return self.name

class Product_Review(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.IntegerField(default=0)
    email=models.EmailField()

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    fname=models.TextField(max_length=155, null=False)
    flname=models.TextField(max_length=155, null=False)
    fcompany=models.TextField(max_length=155, null=False)
    faddress=models.TextField(max_length=155,null=False)
    fTownCity=models.CharField(max_length=155,null=False)
    fCountry=models.TextField(max_length=155,null=False)
    fPostcodeZip=models.CharField(max_length=155,null=False)
    fMobile=models.TextField(max_length=155,null=False)
    Email_filed=models.EmailField(max_length=155,null=False)
    order_note=models.TextField(null=True)
    total_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=155,null=False)
   # order_date=models.DateTimeField(null=max_length=155)
    
class OrderItems(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(null=False)
    price=models.FloatField(null=False)
 
class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    