from .models import Product

def validate_value(input_int):
    max_length = Product.objects.count()

    if input_int > max_length:
        return max_length
    elif input_int < 0:
        return 0
    
    return input_int