"""
author: kp
date: 14/11/16
"""

from django.conf.urls import url
from store import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^product/$', views.ProductView.as_view()),
    url(r'^product/search/$', views.SearchView.as_view()),
]
