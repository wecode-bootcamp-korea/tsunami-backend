from django.http  import JsonResponse
from django.views import View

from .models      import Product, Category, Subcategory, ProductKeyword
from .utils       import validate_value, query_debugger
from users.utils  import check_login

class ProductListView(View):
    @query_debugger
    def get(self, request):    
        try:
            query_strings = request.GET
            limit         = validate_value(int(request.GET.get('limit',500)))
            offset        = validate_value(int(request.GET.get('offset',0))) 

            if not any(query in query_strings for query in ['subcategory','category']):
                products = Product.objects.select_related('maker').all()

            if 'category' in query_strings:
                category      = Category.objects.\
                                prefetch_related('subcategory_set__product_set__maker').\
                                get(id=query_strings['category'])
                subcategories = category.subcategory_set.all()
                products      = [ product for subcategory in subcategories \
                    for product in subcategory.product_set.all() ]

            if 'subcategory' in query_strings:
                subcategory = Subcategory.objects.prefetch_related('product_set__maker').\
                              get(id=query_strings['subcategory'])
                products    = subcategory.product_set.all()

            req_list = [ {
                'id'        : product.id,
                'image_url' : product.main_image_url,
                'name'      : product.name,
                'price'     : int(product.price),
                'maker'     : product.maker.name
             } for product in products[offset:limit] ]

            return JsonResponse({'count':len(list(products)),'product':req_list}, status=200) 
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
        except Category.DoesNotExist:
            return JsonResponse({'MESSAGE':"CATEGORY_DOSENT_EXIST"} ,status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'MESSAGE':"SUBCATEGORY_DOSENT_EXIST"} ,status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"PRODUCT_DOSENT_EXIST"} ,status=400)

class ProductDetailView(View):
    @check_login
    @query_debugger
    def get(self, request, product_id):
        try:
            product     = Product.objects.prefetch_related('productbodycolor_set__color',\
                          'productthickness_set__thickness','productinkcolor_set__color','product_keyword','productoption_set').get(id=product_id)
            body_colors = product.productbodycolor_set.all()
            ink_colors  = product.productinkcolor_set.all()
            nibs        = product.productthickness_set.all()
            user        = getattr(request,'user',None)
            like        = product.userproductlike_set.filter(user=user).first()

            req_dict = {
                'id'            : product.id,
                'image_url'     : product.main_image_url,
                'name'          : product.name,
                'price'         : int(product.price),
                'maker'         : product.maker.name,
                'feature'       : product.feature,
                'origin'        : product.shipping_info.origin,
                'body_colors'   : [ { 'name' : body_color.color.name, 'url': body_color.color.image_url } for body_color in body_colors ]\
                                    if body_colors.exists() else None,
                                    
                'ink_colors'    : [ { 'name' : ink_color.color.name, 'url' : ink_color.color.image_url } for ink_color in ink_colors ]\
                                    if ink_colors.exists() else None,

                'thicknesses'   : [ { 'name':str(nib.thickness.thickness), 'url' : nib.thickness.image_url }  for nib in nibs ]\
                                    if nibs.exists() else  None,

                'keywords'      : [ keyword.keyword for keyword in product.product_keyword.all() ],     
                'options'       : [ option.name for option in  product.productoption_set.all() ],
                'is_like'       : like.is_like if like else None
            }
            return JsonResponse({'product':req_dict}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD_PRODUCT"},status=400)

class MainProductView(View):
    def get(self, request):
        try:
            products = [Product.objects.get(id=70), Product.objects.get(id=71), Product.objects.get(id=86)]

            req_dict = [ {
                'id'            : product.id,
                'imageUrl'      : product.main_image_url,
                'name'          : product.name,
                'price'         : int(product.price),
            } for product in products ]
            return JsonResponse({'product':req_dict},status=200)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD_PRODUCT"},status=400)
