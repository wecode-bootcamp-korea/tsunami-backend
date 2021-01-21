import functools, time

from django.db     import connection, reset_queries
from django.conf   import settings

from orders.models import Cart, Order

def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        print(f"-------------------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print(f"-------------------------------------------------------------------")
        return result
    return wrapper

def refresh_order(obj):
    carts       = obj.cart_set.all().select_related('product')
    total_price = sum([cart.quantity * cart.product.price for cart in carts])

    obj.total_price = total_price
    obj.save()

        