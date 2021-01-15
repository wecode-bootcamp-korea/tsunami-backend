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
    main_image_url = models.URLField(max_length=2000)
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

class Color(models.Model):
    name      = models.CharField(max_length=45)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'colors'

class ProductInkColor(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_ink_colors'

class ProductBodyColor(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    color   = models.ForeignKey('Color', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_body_colors'

class Keyword(models.Model):
    keyword =  models.CharField(max_length=100)

    class Meta:
        db_table = 'keywords'

class ProductKeyword(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    keyword = models.ForeignKey('Keyword', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_keywords'

class Thickness(models.Model):
    thickness = models.DecimalField(max_digits=2, decimal_places=1)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'thickness'

class ProductThickness(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    thickness = models.ForeignKey('Thickness', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_thickness'

class ProductThumbnail(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'product_thumbnails'

class ProductDetailImage(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    image_url = models.URLField(max_length=2000)

    class Meta:
        db_table = 'product_detail_images'

class ProductOption(models.Model):
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)
    name      = models.CharField(max_length=45)
    stock     = models.IntegerField()
    
    class Meta:
        db_table = 'product_options'
