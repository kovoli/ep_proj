import os, sys, unidecode
import django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ep_proj.settings')
django.setup()
from django.db import IntegrityError
import xml.etree.cElementTree as ET


from shop.models import Product, Category, Vendor, Price

# For images
from django.core.files.base import ContentFile
from io import BytesIO
from urllib.request import urlopen

import re

# Бытовая техника
#tree = ET.parse('xml_imports/10500.xml')
tree = ET.parse('xml_imports/10500.xml')
root = tree.getroot()

categories = root.findall('.//category')


cat_db = Category.objects.values('id', 'name')


def check_field_not_none(field):
    if field is not None:
        return field
    else:
        return None



# Helper Functions
def description_beautify(text):
    if text == None:
        return 'С подробным описанием товара и ценами можно ознакомиться на сайте продавца.'
    else:
        regex = r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\:)\s"
        subst = "</br>"
        return re.sub(regex, subst, text, 0, re.MULTILINE)

def param_dict(param):
    param_dict = {}
    for par in param:
        if 'unit' in par.attrib:
            param_dict[par.attrib['name']] = [par.text, par.attrib['unit']]
        else:
            param_dict[par.attrib['name']] = [par.text]
    return param_dict


def def_category(category_id):
    id_cat_name = root.find(".//category[@id='{}']".format(category_id))  # Нахожу катеорию через id в загруженном xml
    id_cat_name = id_cat_name.text
    for i in Category.objects.values('id', 'name'):  # Извлекаю из базы данных все категории и ищу соответствующую категорию
        if i['name'] == id_cat_name:
            return i['id']

def vendor_get_or_create(vendor):
    change_vendor_name = {'Bosch GmbH': 'Bosch', 'Bosch GmbH,Bosch': 'Bosch'}
    if vendor in change_vendor_name:
        vendor = change_vendor_name[vendor]
    elif vendor == None:
        return None
    try:
        return Vendor.objects.get(name=vendor.lower())
    except Vendor.DoesNotExist:
        obj = Vendor(name=vendor.lower())
        return obj.save()


def add_price_to_product(off, product):
    offer_price_data = {'price': 0, 'oldprice': None, 'name': None, 'url': None, 'sales_notes': None,
                        'shop_id': 1, 'product_id': product.id}
    for data in offer_price_data.keys():
        if off.find(data) is None:
            continue
        if data == 'url':
            offer_price_data[data] = 'https://f.gdeslon.ru/cf/0c7e8158ad?mid=12027&goto=' + off.find(data).text[:off.find(data).text.index('?')]
        else:
            offer_price_data[data] = off.find(data).text

    return Price.objects.create(**offer_price_data)

def video_rewiew_param(param):
    youtube_url = 'https://www.youtube.com/embed/'
    for par in param:
        if par.attrib['name'] == 'Видеообзор':
            a = par.text
            return youtube_url + a[a.index('=') + 1:]
    return None




print(len(root.findall('.//offer')))
succers_writes = 0
errors = []
error_count = 0
for off in root.findall('.//offer'):

    product_data = {'name': None, 'description': None,
                    'param': None, 'vendorCode': None,
                    'barcode': None, 'categoryId': None,
                    }
    try:
        for data in product_data.keys():
            if off.find(data) is None:
                continue
            if data == 'description':
                product_data[data] = description_beautify(off.find(data).text)
            elif data == 'param':
                product_data[data] = param_dict(off.findall(data))
            elif data == 'categoryId':
                del product_data['categoryId']
                product_data['category_id'] = def_category(off.find(data).text)
            else:
                product_data[data] = off.find(data).text

        vendor = vendor_get_or_create(off.find('vendor').text)
        video = video_rewiew_param(off.findall('param'))
        #original_picture = check_field_not_none(off.find('picture').text)
        #input_file = BytesIO(urlopen(original_picture, ).read())

        product = Product.objects.create(**product_data)
        product.vendor = vendor
        product.video = video
        add_price_to_product(off, product)

        #product.product_image.save(product_data['name'] + '.jpg', ContentFile(input_file.getvalue()), save=False)
        product.save()
        succers_writes += 1

    except Exception as error:
        error_count += 1
        errors.append(error)
        print(error)

print(succers_writes)
print(len(root.findall('.//offer')))
print(error_count)
print(errors)