from .models import Product

def validate_value(input_int):
    value      = int(input_int)
    max_length = Product.objects.all().count()

    if value > max_length:
        return max_length
    elif value < 0:
        return 0
    
    return value