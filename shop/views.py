from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Vendor
from .forms import CommentForm
from django.db.models import Min, Max, Count
#from . import helpers
from watson import search as watson
from django.db.models import F

def home_page(request):
    favorites_cat = Category.objects.filter(favorites=True)
    list_pro = Product.objects.all().annotate(min_price=Min('prices__price')).order_by('-views')[:12]

    return render(request, 'home_page.html', {'favorites_cat': favorites_cat,
                                              'list_pro': list_pro})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    breadcrumbs = Category.get_ancestors(product.category)
    product.views = F('views') + 1
    product.save()
    product.refresh_from_db(fields=['views'])
    semilar_products = Product.objects.filter(category=product.category) \
                           .exclude(id=product.id) \
                           .annotate(min_price=Min('prices__price')).order_by('-views')[:10]

    comments = product.comments.filter(active=True)
    min_max_price = product.prices.aggregate(min=Min('price'), max=Max('price'), shops=Count('shop_id'))
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
            return redirect('shop:product_detail', slug=product.slug)

    else:
        comment_form = CommentForm()

    return render(request, 'shop/single_product.html', {'product': product,
                                                        'breadcrumbs': breadcrumbs,
                                                        'comments': comments,
                                                        'new_comment': new_comment,
                                                        'comment_form': comment_form,
                                                        'semilar_products': semilar_products,
                                                        'min_max_price': min_max_price})


def category_catalog(request, slug=None):
    return render(request, 'shop/category_product_list.html')

