from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.db import IntegrityError
from unidecode import unidecode


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        category = Category.objects.get(name='Электрические чайники')
        print(category.attribute.all())
        print(category)



# todo Доделать синя