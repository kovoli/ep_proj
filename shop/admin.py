from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, Category, Price, Shop, Vendor, Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'vendor']
    readonly_fields = ['slug']
    search_fields = ['name', 'barcode', 'vendorCode']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('name', 'body')
    list_editable = ('active', )
    readonly_fields = ['product']


@admin.register(Price)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['shop', 'name']
    #readonly_fields = ['product']
    search_fields = ['name']
    list_filter = ('shop', )


@admin.register(Shop)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name']



@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    readonly_fields = ('slug',)
    search_fields = ['name']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['slug']
    search_fields = ['name']