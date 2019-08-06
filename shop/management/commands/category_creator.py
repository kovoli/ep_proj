from django.core.management.base import BaseCommand
import xml.etree.cElementTree as ET
from shop.models import Category
from django.db import IntegrityError
from unidecode import unidecode

def open_cat_xml(file):
    tree = ET.parse(f'./shop/management/category_xml/{file}')
    get_root = tree.getroot()
    return get_root

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='The txt file that contains the journal titles.')

    def handle(self, *args, **kwargs):
        root = open_cat_xml(kwargs['file_name'])
        print(len(root.findall('.//category')))
        for cat in root.findall('.//category'):
            try:
                category_name = cat.text
                if 'parentId' not in cat.attrib:
                    Category.objects.get_or_create(name=category_name)

                else:
                    parent_id = cat.attrib['parentId']
                    parent_category = root.find(f".//category[@id='{parent_id}']").text
                    parent_category_instanz = Category.objects.get(name=parent_category)
                    Category.objects.get_or_create(name=category_name, parent=parent_category_instanz)
                    self.stdout.write(self.style.SUCCESS(f'Подкатегория созданна: {category_name}'))
            except IntegrityError:
                Category.objects.get_or_create(name=category_name, parent=parent_category_instanz, slug=f'{unidecode(category_name.lower())}-{unidecode(parent_category.replace(" ", "-").lower())}')

            except Exception as a:
                self.stdout.write(self.style.ERROR(a))

        self.stdout.write(self.style.SUCCESS('Финиш'))

