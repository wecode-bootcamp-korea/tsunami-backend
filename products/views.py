from django.shortcuts import render

from django.views import View
from django.http  import JsonResponse

from .models      import Product, Category, Subcategory

class ProductListView(View):

    def get(self, request):    
        try:
            query_strings = request.GET
            if not query_strings:
                products = Product.objects.all()
            
            if 'category' in query_strings:
                category      = Category.objects.get(id=query_strings['category'])
                subcategories = category.subcategory_set.all()
                products      = [ product for subcategory in subcategories \
                     for product in subcategory.product_set.all() ]

            if 'subcategory' in query_strings:
                subcategory = Subcategory.objects.get(id=query_strings['subcategory'])
                products    = subcategory.product_set.all()

            req_list = [ {
                'id'        : product.id,
                'image_url' : product.main_image_url,
                'name'      : product.name,
                'price'     : int(product.price),
                'maker'     : product.maker.name
             } for product in products ]

            return JsonResponse({'PRODUCT':req_list}, status=200)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
        except UnboundLocalError:
            return JsonResponse({'MESSAGE':"UNBOUND_LOCAL_ERROR"} ,status=400)
        except Category.DoesNotExist:
            return JsonResponse({'MESSAGE':"CATEGORY_DOSENT_EXIST"} ,status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'MESSAGE':"SUBCATEGORY_DOSENT_EXIST"} ,status=400)

class ProductDetailView(View):
    def get(self, request):

        try:
            product_id = request.GET.get("product_id")
            product    = Product.objects.get(id=product_id)
            req_list   = [
                {
                    'id'            : product.id,
                    'image_url'     : product.main_image_url,
                    'name'          : product.name,
                    'price'         : int(product.price),
                    'maker'         : product.maker.name,
                    'feature'       : product.feature,
                    'origin'        : product.shipping_info.origin,
                    'shipping_info' : product.shipping_info.shipping_info,
                    'shipping_fee'  : int(product.shipping_info.shipping_fee)
                }
            ]
            
            return JsonResponse({'PRODUCT':req_list}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD_PRODUCT"},status=400)
        
