import json

from django.http     import JsonResponse
from django.views    import View

from users.models    import Destination
from products.models import Product, ProductOption
from .models         import Order, Cart, Status
from users.utils     import login_required
from orders.utils    import refresh_order, query_debugger

class CartView(View):
    @query_debugger
    @login_required
    def post(self, request):
        try:
            data           = json.loads(request.body)
            quantity       = data['quantity']
            product        = Product.objects.get(id=data['product'])
            user           = getattr(request,'user',None)
            before_execute = Status.objects.get(id=1)
            option         = product.productoption_set.get(id=data['option'])

            if getattr(user.order_set.last(),'status',None) != before_execute:
                Order.objects.create(
                    user=user,
                    shipping_memo="",
                    total_price=0,
                    status=before_execute
                )
            order = Order.objects.last()

            if Cart.objects.filter(product=product, product_option=option, order=order).exists():
                return JsonResponse({'MESSAGE':'CART_ALREADY_EXISTS'}, status=400)

            Cart.objects.create(
                product=product,
                quantity=quantity,
                order=user.order_set.last(),
                product_option=option
            )
            refresh_order(order)
            return JsonResponse({"MESSAGE":'SUCCESS'},status=200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({'MESSAGE':"PRODUCT_OPTION_DOSENT_EXIST"} ,status=400)

    @query_debugger
    def patch(self, request):
        try:
            data = json.loads(request.body)
            cart = Cart.objects.select_related('product','order').get(id=data['cart_id'])

            if data.get('quantity'):
                cart.quantity = data.get('quantity')
            
            if data.get('option'):
                option              = cart.product.productoption_set.get(id=data['option'])
                cart.product_option = option
            cart.save()

            refresh_order(cart.order)
            return JsonResponse({'MESSAGE':"UPDATED"},status=200)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"PRODUCT_DOSENT_EXIST"} ,status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({'MESSAGE':"PRODUCT_OPTION_DOSENT_EXIST"} ,status=400)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'MESSAGE': 'TYPE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE_ERROR'}, status=400)

class OrderView(View):
    @login_required
    def post(self, request):
        try:
            data                = json.loads(request.body)
            user                = getattr(request,'user',None)
            order               = Order.objects.last()
            after_execute       = Status.objects.get(id=2)
            default_destination = user.destination_set.filter(is_default=True)
            order.shipping_memo = data['shipping_memo']

            if data.get('destination'):
               destination = Destination(user=user, **data['destination'])
               destination.save()

            order.destination = default_destination\
                                    if default_destination.exists() else Destination.objects.last()
            
            order.status      = after_execute
            order.save()

            return JsonResponse({'MESSAGE':'ORDER_EXECUTED'},status=200)
        except ValueError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
