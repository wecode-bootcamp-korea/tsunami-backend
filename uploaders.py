import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tsunami.settings")
django.setup()

from products.models import (
    Category, Subcategory, Maker, ShippingInfo, Product,
    Color, ProductBodyColor, ProductInkColor
)



def categories_uploader():

    categories    = [
        '프리미엄 펜','펜/펜슬','마카','컬러링/브러쉬','디자인 문구'
    ]
    subcategoreis = [
        ['153프리미엄','데스크펜/스마트펜','파카','카렌디쉬','카웨코','매뉴스크립트'],
        ['볼펜','수성펜/사인펜','연필/샤프','형광펜'],
        ['네임펜/유성매직','생활/보드마카','패브릭/세라믹마카'],
        ['컬러링펜','브러쉬펜','미술용품'],
        ['몰스킨','다이어리/노트','카드/봉투','파우치','풀/스티커/테이프','스탬프','데스크용품','모나미 MD상품']
    ]

    for i,category in enumerate(categories):
        print(category)
        Category.objects.create(name=category)
        cat = Category.objects.get(name=category)
        for subcategory in subcategoreis[i]:
            Subcategory.objects.create(name=subcategory, category=cat)
            print(subcategory,end=' ')

def makers_uploader():

    makers = ['Tsunami/쓰나미', 'Fournami/포나미', 'Wecode/위코드','Tori/토리하우스']
    for maker in makers:
        Maker.objects.create(name=maker)

def shipping_info_uploader():
    origin           = ["대한민국/(주)쓰나미","대한민국/(주)포나미","대한민국/(주)위코드","미국/(주)토리하우스",]
    shipping_fee     = 2500
    shipping_info    = "17시이전 주문시 당일출고(공휴일,토/일요일제외)"
    shipping_company = ["쓰나미배송","포나미배송", "위코드배송", "토리하우스 배송"]

    for i in range(4):
        ShippingInfo.objects.create(
            origin=origin[i],
            shipping_fee=shipping_fee,
            shipping_info=shipping_info,
            shipping_company=shipping_company[i]
        )

def product_uploader():
    image_urls = [
        'https://images.unsplash.com/photo-1448471237638-f8ccc7d5ac9d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NDV8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1588850561139-208fa7795392?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NTZ8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=100&amp;q=60',
        'https://images.unsplash.com/photo-1581309659338-8e6fc3fa06fe?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTd8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1601311911926-dbdae16e54c9?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
    ]
    name       = [
        '153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트'
    ]
    price      = [
        '15000','7900','36000','5500'
    ]
    feature    = [
        '블랙 샤프 아주 좋아요','2018년 올해의 색상의 펜', '100년 전통 피카 만년필', '세가지 색상을 한번에'
    ]
    description = [
        '리필용 심 포함', 'Ultra Violet', '100년 전통의 피카 만년필', '세가지 색, 세번의 감동'
    ]
    subcategory = [
        '153프리미엄','볼펜', '파카', '형광펜'
    ]

    maker         = Maker.objects.get(id=1)
    shipping_info = ShippingInfo.objects.get(id=1)
    for i in range(4):
        sub_cat = Subcategory.objects.get(name=subcategory[i])
        Product.objects.create(
            name=name[i],
            price=price[i],
            feature=feature[i],
            description=description[i],
            maker=maker,
            shipping_info=shipping_info,
            main_image_url=image_urls[i],
            subcategory=sub_cat,    
        )

def product_uploader2():
    image_urls = [
        'https://images.unsplash.com/photo-1448471237638-f8ccc7d5ac9d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NDV8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1588850561139-208fa7795392?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NTZ8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=100&amp;q=60',
        'https://images.unsplash.com/photo-1581309659338-8e6fc3fa06fe?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTd8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1601311911926-dbdae16e54c9?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1448471237638-f8ccc7d5ac9d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NDV8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1588850561139-208fa7795392?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NTZ8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=100&amp;q=60',
        'https://images.unsplash.com/photo-1581309659338-8e6fc3fa06fe?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTd8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1601311911926-dbdae16e54c9?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1448471237638-f8ccc7d5ac9d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NDV8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1588850561139-208fa7795392?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NTZ8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=100&amp;q=60',
        'https://images.unsplash.com/photo-1581309659338-8e6fc3fa06fe?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTd8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1601311911926-dbdae16e54c9?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1448471237638-f8ccc7d5ac9d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NDV8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1588850561139-208fa7795392?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NTZ8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=100&amp;q=60',
        'https://images.unsplash.com/photo-1581309659338-8e6fc3fa06fe?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTd8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1601311911926-dbdae16e54c9?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1448471237638-f8ccc7d5ac9d?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NDV8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1588850561139-208fa7795392?ixid=MXwxMjA3fDB8MHxzZWFyY2h8NTZ8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=100&amp;q=60',
        'https://images.unsplash.com/photo-1581309659338-8e6fc3fa06fe?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTd8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
        'https://images.unsplash.com/photo-1601311911926-dbdae16e54c9?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTF8fHBlbnxlbnwwfHwwfA%3D%3D&amp;ixlib=rb-1.2.1&amp;auto=format&amp;fit=crop&amp;w=200&amp;q=60',
    ]
    name       = [
        '153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트','153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트','153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트','153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트','153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트'
    ]
    price      = [
        '15000','7900','36000','5500','15000','7900','36000','5500','15000','7900','36000','5500','15000','7900','36000','5500','15000','7900','36000','5500'
    ]
    feature    = [
        '블랙 샤프 아주 좋아요','2018년 올해의 색상의 펜', '100년 전통 피카 만년필', '세가지 색상을 한번에','블랙 샤프 아주 좋아요','2018년 올해의 색상의 펜', '100년 전통 피카 만년필', '세가지 색상을 한번에','블랙 샤프 아주 좋아요','2018년 올해의 색상의 펜', '100년 전통 피카 만년필', '세가지 색상을 한번에','블랙 샤프 아주 좋아요','2018년 올해의 색상의 펜', '100년 전통 피카 만년필', '세가지 색상을 한번에','블랙 샤프 아주 좋아요','2018년 올해의 색상의 펜', '100년 전통 피카 만년필', '세가지 색상을 한번에'
    ]
    description = [
        '리필용 심 포함', 'Ultra Violet', '100년 전통의 피카 만년필', '세가지 색, 세번의 감동','리필용 심 포함', 'Ultra Violet', '100년 전통의 피카 만년필', '세가지 색, 세번의 감동','리필용 심 포함', 'Ultra Violet', '100년 전통의 피카 만년필', '세가지 색, 세번의 감동','리필용 심 포함', 'Ultra Violet', '100년 전통의 피카 만년필', '세가지 색, 세번의 감동','리필용 심 포함', 'Ultra Violet', '100년 전통의 피카 만년필', '세가지 색, 세번의 감동'
    ]
    subcategory = [
        '카렌디쉬','카웨코','데스크펜/스마트펜','매뉴스크립트','수성펜/사인펜','연필/샤프', '네임펜/유성매직','생활/보드마카','패브릭/세라믹마카','컬러링펜','브러쉬펜','미술용품','몰스킨','다이어리/노트','카드/봉투','파우치','풀/스티커/테이프','스탬프','데스크용품','모나미 MD상품'
    ]

    maker         = Maker.objects.get(id=1)
    shipping_info = ShippingInfo.objects.get(id=1)
    for i in range(20):
        sub_cat = Subcategory.objects.get(name=subcategory[i])
        Product.objects.create(
            name=name[i],
            price=price[i],
            feature=feature[i],
            description=description[i],
            maker=maker,
            shipping_info=shipping_info,
            main_image_url=image_urls[i],
            subcategory=sub_cat,    
        )

def color_uploader():
    color_names = ['레드','블랙','블루','핑크','바이올렛','코랄','마젠타','시안','옐로우']
    url = "https://d1bg8rd1h4dvdb.cloudfront.net/upload/imgServer/product/attribute/23_58724_P_120x80_20190422180922.blob"

    for color_name in color_names:
        Color.objects.create(name=color_name, image_url=url)


def colorink_uploader():
    names = [ '153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트']

    for name in names:
        products = Product.objects.filter(name=name)
        
        for product in products:
            if name == '153 블랙 샤프 세트':
                ProductInkColor.objects.create(product=product, color=Color.objects.get(name="블랙"))
            elif name == '올해의 색상 프리미엄 펜':
                ProductInkColor.objects.create(product=product, color=Color.objects.get(name="마젠타"))
            elif name == '피카 만년필':
                ProductInkColor.objects.create(product=product, color=Color.objects.get(name="블랙"))
            elif name == '삼색 형광펜 세트':
                ProductInkColor.objects.create(product=product, color=Color.objects.get(name="블루"))
                ProductInkColor.objects.create(product=product, color=Color.objects.get(name="옐로우"))
                ProductInkColor.objects.create(product=product, color=Color.objects.get(name="마젠타"))




def colorbody_uploader():
    names = [ '153 블랙 샤프 세트', '올해의 색상 프리미엄 펜', '피카 만년필', '삼색 형광펜 세트']

    for name in names:
        products = Product.objects.filter(name=name)
        
        for product in products:
            if name == '153 블랙 샤프 세트':
                ProductBodyColor.objects.create(product=product, color=Color.objects.get(name="블랙"))
            elif name == '올해의 색상 프리미엄 펜':
                ProductBodyColor.objects.create(product=product, color=Color.objects.get(name="마젠타"))
            elif name == '피카 만년필':
                ProductBodyColor.objects.create(product=product, color=Color.objects.get(name="블랙"))
            elif name == '삼색 형광펜 세트':
                ProductBodyColor.objects.create(product=product, color=Color.objects.get(name="블루"))
                ProductBodyColor.objects.create(product=product, color=Color.objects.get(name="옐로우"))
                ProductBodyColor.objects.create(product=product, color=Color.objects.get(name="마젠타"))


colorbody_uploader()
