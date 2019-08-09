from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# for slugfield
from django.urls import reverse
from django.template.defaultfilters import slugify
from unidecode import unidecode

from ckeditor.fields import RichTextField
# Images
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit

from django.contrib.postgres.fields import JSONField


# ----------- CATEGORY -------------
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = RichTextField(blank=True, null=True)
    category_image = ProcessedImageField(upload_to='category_images/%Y/%m',
                                         processors=[ResizeToFit(None, 250)],
                                         format='JPEG',
                                         options={'quality': 80},
                                         blank=True,
                                         max_length=250)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category_catalog', args=[self.slug])

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['-name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [models.Index(fields=['slug'])]


# -------------- SHOP ---------------
class Shop(models.Model):
    name = models.CharField(max_length=100)
    image_store = ProcessedImageField(upload_to='shop_image/',
                                      blank=True,
                                      processors=[ResizeToFit(80, None)],
                                      format='JPEG',
                                      options={'quality': 100})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


# ------------ VENDOR ---------------
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = RichTextField(blank=True)
    image_vendor = ProcessedImageField(upload_to='vendor_image/',
                                       blank=True,
                                       processors=[ResizeToFit(200, 200)],
                                       format='JPEG',
                                       options={'quality': 80})

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:vendor', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super(Vendor, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        indexes = [models.Index(fields=['slug'])]


# ------------ PRODUCT -------------
class Product(models.Model):
    name = models.CharField(max_length=255)
    offer_id = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = RichTextField(blank=True, null=True)
    param = JSONField(blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    barcode = models.CharField(max_length=30, blank=True, null=True)
    vendorCode = models.CharField(max_length=150, blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    product_image = ProcessedImageField(upload_to='product_images/%Y/%m',
                                        processors=[ResizeToFit(None, 350)],
                                        format='JPEG',
                                        options={'quality': 80},
                                        blank=True,
                                        max_length=250)
    product_image_grid = ImageSpecField(source='product_image',
                                        processors=[ResizeToFit(None, 160)],
                                        format='JPEG',
                                        options={'quality': 90})
    product_image_category = ImageSpecField(source='product_image',
                                            processors=[ResizeToFit(None, 239)],
                                            format='JPEG',
                                            options={'quality': 90})

    # related_models
    category = TreeForeignKey('Category', related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendor', related_name='vendors', on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [models.Index(fields=['name', 'slug']),
                   models.Index(fields=['barcode']),
                   models.Index(fields=['vendorCode'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name) + f'-{self.offer_id}')
        super(Product, self).save(*args, **kwargs)


# ------------ PRICE --------------
class Price(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    oldprice = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    name = models.CharField(max_length=255)
    url = models.TextField(max_length=300)
    sales_notes = models.CharField(max_length=255, blank=True, null=True)
    # relate_models
    shop = models.ForeignKey(Shop, related_name='shops', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='prices', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        ordering = ['price']
        indexes = [models.Index(fields=['product', 'shop'])]


# ------------ PRODUCT COMMENT -------------
class Comment(models.Model):
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    positiv = models.TextField(blank=True)
    negativ = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return 'Комментарий от {} {}'.format(self.name, self.product)

# TODO: Добавить ID к модели продуктов
# TODO: Сделать Slug + ArticleID
