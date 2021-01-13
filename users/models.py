from django.db import models

class User(models.Model):
    name            = models.CharField(max_length=45)
    username        = models.CharField(max_length=20, unique=True)
    password        = models.CharField(max_length=100)
    email           = models.EmailField(max_length=60, unique=True)
    phone_number    = models.CharField(max_length=11)
    birthday        = models.DateField(null=True)
    is_sms_agreed   = models.BooleanField()
    is_email_agreed = models.BooleanField()
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = "users"

class Destination(models.Model):
    name           = models.CharField(max_length=45)
    phone_number   = models.CharField(max_length=11)
    user           = models.ForeignKey('User', on_delete=models.CASCADE)
    is_default     = models.BooleanField()
    zipcode        = models.CharField(max_length=5)
    street_name    = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100)

    class Meta:
        db_table = 'destinations'
