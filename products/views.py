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
            return JsonResponse({'MESSAGE':"KEY_ERROR"} ,status=400)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
        except UnboundLocalError:
            return JsonResponse({'MESSAGE':"UNBOUND_LOCAL_ERROR"} ,status=400)
        except Category.DoesNotExist:
            return JsonResponse({'MESSAGE':"CATEGORY_DOSENT_EXIST"} ,status=400)
        except Subcategory.DoesNotExist:
            return JsonResponse({'MESSAGE':"SUBCATEGORY_DOSENT_EXIST"} ,status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"PRODUCT_DOSENT_EXIST"} ,status=400)

class ProductDetailView(View):
    def get(self, request, product_id):

        try:
            product     = Product.objects.get(id=product_id)
            body_colors = product.productbodycolor_set.all()
            ink_colors  = product.productinkcolor_set.all()
            nibs        = product.productthickness_set.all()

            

            body_color_list, ink_color_list, thickness_list = ([] for _ in range(3))
            
            if body_colors.exists():
                body_color_list = [
                    { body_color.color.name : body_color.color.image_url } for body_color in body_colors
                ]

            if ink_colors.exists():
                ink_color_list = [
                    { ink_color.color.name : ink_color.color.image_url } for ink_color in ink_colors
                ]

            if nibs.exists():
                thickness_list = [
                    { str(nib.thickness.thickness) : nib.thickness.image_url }  for nib in nibs
                ]
  
            req_dict = {
                'id'            : product.id,
                'image_url'     : product.main_image_url,
                'name'          : product.name,
                'price'         : int(product.price),
                'maker'         : product.maker.name,
                'feature'       : product.feature,
                'origin'        : product.shipping_info.origin,
                'body_colors'   : body_color_list,
                'ink_colors'    : ink_color_list,
                'thicknesses'   : thickness_list,      
            }
            return JsonResponse({'PRODUCT':req_dict}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status=400)
        except ValueError:
            return JsonResponse({'MESSAGE':'VALUE_ERROR'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVAILD_PRODUCT"},status=400)