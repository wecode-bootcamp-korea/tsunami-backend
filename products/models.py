from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Subcategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name     = models.CharField(max_length=45)

    class Meta:
        db_table = 'subcategories'

class Product(models.Model):
    name           = models.CharField(max_length=45)
    subcategory    = models.ForeignKey('Subcategory', on_delete=models.CASCADE)
    feature        = models.TextField(null=True)
    price          = models.DecimalField(max_digits=8, decimal_places=2)
    shipping_info  = models.ForeignKey('ShippingInfo', null=True, on_delete=models.SET_NULL)
    maker          = models.ForeignKey('Maker', null=True, on_delete=models.SET_NULL)
    description    = models.CharField(max_length=100, null=True)
    main_image_url = models.CharField(max_length=2000)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

class ShippingInfo(models.Model):
    origin           = models.CharField(max_length=45)
    shipping_info    = models.CharField(max_length=45)
    shipping_fee     = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_company = models.CharField(max_length=45)

    class Meta:
        db_table = 'shipping_infos'

class Maker(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'makers'
