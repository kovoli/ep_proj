from django.shortcuts import render
from .models import Category



# ---------- HELPER FUNCTIONS -----------------------
def menu():
    categories_nav = Category.objects.all()
    return categories_nav


def home_page(request):

    return render(request, 'home_page.html', {'categories': menu()})


def category_catalog(request, slug=None):
    return render(request, 'shop/category_product_list.html', {'categories': menu()})

