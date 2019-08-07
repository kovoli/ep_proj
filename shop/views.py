from django.shortcuts import render
from .models import Category






def home_page(request):

    return render(request, 'home_page.html')


def category_catalog(request, slug=None):
    return render(request, 'shop/category_product_list.html')

