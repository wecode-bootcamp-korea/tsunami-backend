from django.db import models

class User(models.Model):
    
    name           = models.CharField(max_length=45)
    username       = models.CharField(max_length=20, unique=True)
    password       = models.CharField(max_length=100)
    email          = models.EmailField(max_length=60, unique=True)
    phone_number   = models.CharField(max_length=11)
    birthday       = models.CharField(max_length=12, null=True) # form : '19xx, 08, 15'
    sms_agree      = models.BooleanField()
    email_agree    = models.BooleanField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = "users"

class Destination(models.Model):

    name                = models.CharField(max_length=45)
    phone_number        = models.CharField(max_length=11)
    user                = models.ForeignKey('User', on_delete=models.CASCADE)
    default_destination = models.BooleanField()
    zipcode             = models.CharField(max_length=5)
    street_name         = models.CharField(max_length=45)
    detail_address      = models.CharField(max_length=45)

    class Meta:
        db_table = 'destinations'
