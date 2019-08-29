from django.urls import path, include
from . import views


app_name = 'Shop'

urlpatterns = [
    # Shop_app urls include
    path('', views.home_page, name='home'),
    # ------ SHOP URLS -------
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('catalog/<slug:slug>/', views.category_catalog, name='category_catalog'),
    path('search/', views.search_products, name='search_products'),
    # ------ VENDOR URLS -----
    path('vendors/', views.vendor_list, name='vendore_list'),
    path('vendor_categories/<slug:slug_vendor>/', views.vendor_category_list, name='vendor'),
    path('vendor/<slug:slug_vendore>/<slug:slug_category>/', views.vendor_product_list, name='vendor_product_list'),
]