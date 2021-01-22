import json

from django.http  import JsonResponse
from django.views import View

from users.models import User
from products.models import Product

from users.utils   import login_required
from products.utils import query_debugger
from orders.models import Order, Cart


class CartView(View):
    @login_required
    @query_debugger
    def get(self, request):
        try:
            user = request.user
            orders = Order.objects.filter(user=user, status=1)

            if not orders.exists():
                return JsonResponse({"carts_list": {[]}}, status=200)

            order = orders.get()
            carts = Cart.objects.filter(order=order).select_related("product_option__product__shipping_info")
            
            carts_list= [{
                "cart_id"         : cart.id,
                "product_name"    : cart.product_option.product.name, 
                "product_option"  : cart.product_option.name, 
                "options"         : [{option.id: option.name}
                    for option in cart.product_option.product.productoption_set.all()],
                "mail_image_url"  : cart.product_option.product.main_image_url,
                "price"           : float(cart.product_option.product.price), 
                "quantity"        : cart.quantity,
                "shipping_company": cart.product_option.product.shipping_info.shipping_company,
                "shipping_fee"    : float(cart.product_option.product.shipping_info.shipping_fee)
                } for cart in carts ]
            return JsonResponse({"carts_list": carts_list}, status=200)
        except ValueError:
            return JsonResponse({"MESSAGE": "VALUE_ERROR"}, status=400)

    @login_required
    def delete(self, request):
        try: 
            data = json.loads(request.body)
            cart_id = data["cart_id"]
            
            if not isinstance(cart_id, int):
                return JsonResponse({"MESSAGE": "INVALID_ID"}, statu=400)
            
            if not Cart.objects.filter(id=cart_id).exists():
                return JsonResponse({"MESSAGE": "INVALID_ID"}, status=400)

            Cart.objects.get(id=cart_id).delete()
            return JsonResponse({"MESSAGE": "DELETED"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
