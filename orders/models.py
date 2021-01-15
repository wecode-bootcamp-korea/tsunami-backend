from django.db import models

class Order(models.Model):
    user          = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)
    destination   = models.ForeignKey('users.destination', null=True ,on_delete=models.SET_NULL)
    shipping_memo = models.CharField(max_length=100)
    total_price   = models.DecimalField(max_digits=10,decimal_places=2)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    product_option = models.ForeignKey('products.ProductOption', null=True, on_delete=models.SET_NULL)
    quantity       = models.IntegerField()
    order          = models.ForeignKey('Order', null=True, on_delete=models.CASCADE)
    product        = models.ForeignKey('products.Product', null=True, on_delete=models.SET_NULL)
    user           = models.ForeignKey('users.User', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'carts'