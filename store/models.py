from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Product(models.Model):
    SERIALIZATION_FIELDS = (
        'title', 'description', 'brand', 'thumbnail', 'sku', 'mrp', 'mrp',
        'available_price', 'discount', 'offers', 'shipping_charges',
        'cashback', 'category', 'subcategory', 'seller', 'stock',
        'variant', 'country', 'warranty', 'shipping_time')

    title = models.CharField(max_length=512)
    description = models.TextField()
    brand = models.CharField(max_length=256)
    thumbnail = models.TextField()
    sku = models.CharField(max_length=256)
    mrp = models.FloatField()
    available_price = models.FloatField()
    discount = models.FloatField()
    offers = models.CharField(max_length=512)
    shipping_charges = models.CharField(max_length=512)
    cashback = models.CharField(max_length=512)
    category = models.CharField(max_length=256)
    subcategory = models.CharField(max_length=256)
    seller = models.CharField(max_length=512)
    stock = models.CharField(max_length=64)
    variant = models.CharField(max_length=512)
    country = models.CharField(max_length=256)
    warranty = models.CharField(max_length=512)
    shipping_time = models.CharField(max_length=512)
    urlh = models.CharField(max_length=64)
    crawl_time = models.DateTimeField()
    crawl_date = models.DateField()
    source = models.CharField(max_length=128)
    url = models.CharField(max_length=1024)
    price_change = models.FloatField()
    timestamp = models.DateTimeField()
    others = models.TextField()
    meta = models.TextField()
    rank = models.IntegerField()
