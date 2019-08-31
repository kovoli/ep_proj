from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Vendor
from .forms import CommentForm, FilterForm
from django.db.models import Min, Max, Count
from . import helpers
from watson import search as watson
from django.db.models import F


def home_page(request):
    favorites_cat = Category.objects.filter(favorites=True)
    list_pro = Product.objects.all().annotate(min_price=Min('prices__price')).order_by('-views')[:12]

    return render(request, 'home_page.html', {'favorites_cat': favorites_cat,
                                              'list_pro': list_pro})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    breadcrumbs = Category.get_ancestors(product.category, include_self=True)
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
    category = get_object_or_404(Category, slug=slug)
    # -------- Крошки и их потомки
    breadcrumbs = Category.get_ancestors(category, include_self=True)
    # -------- Если уровень категории ниже первой выводятся только категории без товаров
    if category.get_level() <= 1:
        cat = category.get_descendants().order_by('tree_id', 'id', '-name')
        return render(request, 'shop/category_catalog.html', {'category': category,
                                                              'cat': cat,
                                                              'breadcrumbs': breadcrumbs})

    if category.get_level() >= 2:

        category = get_object_or_404(Category, slug=slug)
        cat = category.get_descendants(include_self=True).order_by('tree_id', 'id', 'name')
        last_node = category.get_siblings(include_self=True)

        # -------- Если категория равно уровню два и больше выводяться товары

        list_pro = Product.objects.filter(category__in=Category.objects.get(id=category.id)
                                          .get_descendants(include_self=True))\
                                          .annotate(min_price=Min('prices__price')).order_by('-views')

        vendors_ids = list_pro.values_list('vendor_id', flat=True).order_by().distinct()
        # -------- Форма для фильтрации
        filter_form = FilterForm(request.GET)  # , attr=category.attribute.all()
        filter_form.fields['brand'].queryset = Vendor.objects.filter(id__in=vendors_ids)

        products_list = helpers.pg_records(request, list_pro, 52)
        # ------- Фильтрация по брендам
        if filter_form.is_valid():
            if filter_form.cleaned_data['brand']:
                list_pro = Product.objects.filter(category__in=Category.objects.get(id=category.id) \
                                                  .get_descendants(include_self=True)) \
                    .annotate(min_price=Min('prices__price')) \
                    .filter(vendor__in=filter_form.cleaned_data['brand']).order_by('-views')
                products_list = helpers.pg_records(request, list_pro, 100)
            # ------- Цена от и больше
            if filter_form.cleaned_data['min_price']:
                list_pro = list_pro.filter(prices__price__gte=filter_form.cleaned_data['min_price']).order_by(
                    '-views')
                products_list = helpers.pg_records(request, list_pro, 100)
            # ------- Цена до и меньше
            if filter_form.cleaned_data['max_price']:
                list_pro = list_pro.filter(prices__price__lte=filter_form.cleaned_data['max_price']).order_by(
                    '-views')
                products_list = helpers.pg_records(request, list_pro, 100)
            # ------- Фильтр по цене вверх и вниз и популярность
            if filter_form.cleaned_data['ordering']:
                list_pro = list_pro.order_by(filter_form.cleaned_data['ordering'])
                products_list = helpers.pg_records(request, list_pro, 100)
            """if category.attribute:
                for form_name in filter_form.fields:
                    if filter_form.cleaned_data[form_name]:
                        list_pro = list_pro.filter(value__icontains=filter_form.cleaned_data[form_name])
                        products_list = helpers.pg_records(request, list_pro, 100)"""

            return render(request, 'shop/category_product_list.html', {'products_list': products_list,
                                                                   'category': category,
                                                                   'cat': cat,
                                                                   'last_node': last_node,
                                                                   'breadcrumbs': breadcrumbs,
                                                                   'filter_form': filter_form,
                                                                   })


def search_products(request):
    if 'q' in request.GET:
        q = request.GET['q']
        search_list = watson.filter(Product, q).annotate(min_price=Min('prices__price'))
        products_list = helpers.pg_records(request, search_list, 54)
    return render(request, 'shop/search_products.html', {'q': q,
                                                         'products_list': products_list,
                                                         'search_list': search_list})


# ------------------- VENDOR VIEWS ------------------
def vendor_list(request):
    vandor_alphabet = [ "a","b","c","d","e","f","g","h","i","k",
                        "l","m","n","o","p","q","r","s","t","u",
                        "v","w","x","y","z",]
    vendor_alphabet_rus = ['а', ' б', ' в', ' г', ' д', ' е', ' ё', ' ж', ' з', ' и', ' й', ' к', ' л',
                           ' м', ' н', ' о', ' п', ' р', ' с', ' т', ' у', ' ф', ' х', ' ц', ' ч', ' ш',
                           ' щ', ' ъ', ' ы', ' ь', ' э', ' ю', ' я']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if 'ven' in request.GET:
        ven = request.GET['ven']

        list_vendor = Vendor.objects.filter(name__istartswith=ven)

        return render(request, 'vendors/vendor_list.html', {
                                                        'vandor_alphabet': vandor_alphabet,
                                                        'vendor_alphabet_rus': vendor_alphabet_rus,
                                                        'digits': digits,
                                                        'list_vendor': list_vendor,
                                                        })

    return render(request, 'vendors/vendor_list.html', {
        'vandor_alphabet': vandor_alphabet,
        'digits': digits,
    })


def vendor_category_list(request, slug_vendor):
    vendor = get_object_or_404(Vendor, slug=slug_vendor)
    list_pro = Product.objects.filter(vendor=vendor)
    categories_id_list = list_pro.values_list('category_id', flat=True).order_by().distinct()
    categories = Category.objects.filter(id__in=categories_id_list)

    return render(request, 'vendors/vendor_category_list.html', {'categories': categories,
                                                                 'vendor': vendor})


def vendor_product_list(request, slug_vendore, slug_category):
    vendor = get_object_or_404(Vendor, slug=slug_vendore)
    category = Category.objects.get(slug=slug_category)
    list_pro = Product.objects.filter(category__slug=slug_category)\
                              .filter(vendor=vendor)\
                              .annotate(min_price=Min('prices__price'))

    return render(request, 'vendors/vendor_product_list.html', {'vendor': vendor,
                                                                'category': category,
                                                                'list_pro': list_pro})
