from django.core.management.base import BaseCommand
import xml.etree.cElementTree as ET
from shop.models import Category
from django.db import IntegrityError
from unidecode import unidecode


def open_cat_xml(file):
    tree = ET.parse(f'./shop/management/import_xml/{file}')
    get_root = tree.getroot()
    return get_root


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='The txt file that contains the journal titles.')

    def handle(self, *args, **kwargs):
        root = open_cat_xml(kwargs['file_name'])
        count_created_cat = 0
        for cat in root.findall('.//category'):
            try:
                category_name = cat.text
                if 'parentId' not in cat.attrib:
                    Category.objects.get_or_create(name=category_name)
                    count_created_cat += 1
                else:
                    parent_id = cat.attrib['parentId']
                    parent_category = root.find(f".//category[@id='{parent_id}']").text
                    parent_category_instanz = Category.objects.get(name=parent_category)
                    Category.objects.get_or_create(name=category_name, parent=parent_category_instanz)
                    count_created_cat += 1
            except IntegrityError:
                Category.objects.get_or_create(name=category_name, parent=parent_category_instanz, slug=f'{unidecode(category_name.lower())}-{unidecode(parent_category.replace(" ", "-").lower())}')
                count_created_cat += 1
            except Exception as a:
                self.stdout.write(self.style.ERROR(a))
        all_cat_count = len(root.findall('.//category'))

        self.stdout.write(self.style.SUCCESS(f'Всего категории в XML: {all_cat_count}' ))
        self.stdout.write(self.style.SUCCESS(f'Категорий созданно: {count_created_cat}'))

