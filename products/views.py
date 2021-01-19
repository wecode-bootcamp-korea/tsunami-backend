from django.http  import JsonResponse
from django.views import View

from .models      import Product, Category, Subcategory, ProductKeyword
from .utils       import validate_value, query_debugger
from users.utils  import check_login

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

            return JsonResponse({'product':req_list}, status=200)
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
            likes       = product.userproductlike_set.filter(user=user)
            # colors      = Colors.objects.prefetch_related('').all()


            req_dict = {
                'id'            : product.id,
                'image_url'     : product.main_image_url,
                'name'          : product.name,
                'price'         : int(product.price),
                'maker'         : product.maker.name,
                'feature'       : product.feature,
                'origin'        : product.shipping_info.origin,
                'body_colors'   : [ { body_color.color.name : body_color.color.image_url} for body_color in body_colors ]\
                                    if body_colors.exists() else None,
                                    
                'ink_colors'    : [ { ink_color.color.name : ink_color.color.image_url } for ink_color in ink_colors ]\
                                    if ink_colors.exists() else None,

                'thicknesses'   : [ { str(nib.thickness.thickness) : nib.thickness.image_url }  for nib in nibs ]\
                                    if nibs.exists() else  None,

                'keywords'      : [ keyword.keyword for keyword in product.product_keyword.all() ],     
                'options'       : [ option.name for option in  product.productoption_set.all() ],
                'is_like'       : likes[0].is_like if likes.exists() else None,
            }
            return JsonResponse({'product':req_dict}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD_PRODUCT"},status=400)
