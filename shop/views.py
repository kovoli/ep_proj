from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Vendor
#from .forms import CommentForm, BrandForms
from django.db.models import Min, Max, Count
#from . import helpers
from watson import search as watson
from django.db.models import F

def home_page(request):
    favorites_cat = Category.objects.filter(favorites=True)
    list_pro = Product.objects.all().annotate(min_price=Min('prices__price')).order_by('views')[:12]

    return render(request, 'home_page.html', {'favorites_cat': favorites_cat,
                                              'list_pro': list_pro})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    #product_min_price = product.prices.all().order_by('price')[:1]
    #print(product_min_price.price)
    breadcrumbs = Category.get_ancestors(product.category)
    product.views = F('views') + 1
    product.save()
    product.refresh_from_db(fields=['views'])
    semilar_products = Product.objects.filter(category=product.category) \
                           .exclude(id=product.id) \
                           .annotate(min_price=Min('prices__price')).order_by('-views')[:10]
    min_max_price = product.prices.aggregate(min=Min('price'), max=Max('price'), shops=Count('shop_id'))

    return render(request, 'shop/single_product.html', {'product': product,
                                                        #'product_min_price': product_min_price,
                                                        'breadcrumbs': breadcrumbs,
                                                        #'comments': comments,
                                                        #'new_comment': new_comment,
                                                        #'comment_form': comment_form,
                                                        'semilar_products': semilar_products,
                                                        'min_max_price': min_max_price})


def category_catalog(request, slug=None):
    return render(request, 'shop/category_product_list.html')

