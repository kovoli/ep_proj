from django.core.management.base import BaseCommand
from shop.models import Category, Product, Value
from django.db import IntegrityError
from unidecode import unidecode


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        category = Category.objects.get(name='Электрические чайники')
        print(category.attribute.all())
        print(category)


        products_by_cat = Product.objects.filter(category=category)
        print(products_by_cat.count())
        a = []
        for i in products_by_cat:
            if 'Объем' in i.param.keys():
                a.append(i.param['Объем'][0])
        print(list(set(a)))

        """
        for product in products_by_cat:
            for attr in category.attribute.all():
                if attr.name in product.param.keys():
                    prod_attr = product.param[attr.name][0]
                    try:
                        val = Value.objects.get(name=prod_attr, attribute=attr)
                        val.product.add(product)
                    except Value.DoesNotExist:
                        val = Value.objects.create(name=prod_attr, attribute=attr)
                        val.product.add(product)
                else:
                    continue
"""




# todo Доделать синя
