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
                subcategories = Subcategory.objects.filter(category=category)
                products      = []

                for subcategory in subcategories:
                    product = Product.objects.get(subcategory=subcategory)
                    products.append(product)
                
            if 'subcategory' in query_strings:
                subcategory = Subcategory.objects.get(id=query_strings['subcategory'])
                products    = Product.objects.filter(subcategory=subcategory)

            req_list = []

            for product in products:
                
                req_dict = {
                    'id'          : product.id,
                    'image_url'   : product.main_image_url,
                    'name'        : product.name,
                    'price'       : int(product.price),
                    'maker'       : product.maker.name
                }
                req_list.append(req_dict)
            return JsonResponse({'PRODUCT':req_list}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status=400)

class ProductDetailView(View):
    def get(self, request):

        try:
            product_id = request.GET.get("product_id")
            product = Product.objects.get(id=product_id)
            req_list = []

            req_dict = {
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
            req_list.append(req_dict)
            return JsonResponse({'PRODUCT':req_list}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_PRODUCT"},status=400)
        
