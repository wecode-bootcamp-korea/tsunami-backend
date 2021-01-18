from django.views import View
from django.http  import JsonResponse

from .models      import Product, Category, Subcategory
from .utils       import validate_value

class ProductListView(View):

    def get(self, request):    
        try:
            query_strings = request.GET
            limit         = validate_value(int(request.GET.get('limit',40)))
            offset        = validate_value(int(request.GET.get('offset',0))) 

            if not any(query in query_strings for query in ['subcategory','category']):
                products = Product.objects.all()[offset:limit]

            if 'category' in query_strings:
                category      = Category.objects.get(id=query_strings['category'])
                subcategories = category.subcategory_set.all()
                products      = [ product for subcategory in subcategories \
                     for product in subcategory.product_set.all() ][offset:limit]

            if 'subcategory' in query_strings:
                subcategory = Subcategory.objects.get(id=query_strings['subcategory'])
                products    = subcategory.product_set.all()[offset:limit]

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
        except Category.DoesNotExist:
            return JsonResponse({'MESSAGE':"CATEGORY_DOSENT_EXIST"} ,status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'MESSAGE':"SUBCATEGORY_DOSENT_EXIST"} ,status=400)

class ProductDetailView(View):

    def get(self, request, product_id):
        try:
            product    = Product.objects.get(id=product_id)
            req_dict   = {
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
            return JsonResponse({'PRODUCT':req_dict}, status=200)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD_PRODUCT"},status=400)
        