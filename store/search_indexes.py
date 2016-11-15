"""
author: kp
date: 14/11/16
"""
import datetime
from haystack import indexes
from store.models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='description')
    brand = indexes.CharField(model_attr='brand')
    category = indexes.CharField(model_attr='category')
    subcategory = indexes.CharField(model_attr='subcategory')
    timestamp = indexes.DateTimeField(model_attr='timestamp')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(timestamp__lte=datetime.datetime.now())
