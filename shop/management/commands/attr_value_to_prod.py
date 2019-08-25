from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.db import IntegrityError
from unidecode import unidecode


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        category = Category.objects.get(name='Электрические чайники')
        print(category.attribute.all())
        print(category)


"""products_by_cat = Product.objects.filter(category=category)
   for product in product_by_cat:
       for attr in category.attribute.all():        

"""



# todo Доделать синя
