"""
author: kp
date: 16/11/16
"""

from django.http import HttpResponseRedirect


def index(request):
    return HttpResponseRedirect("/store/")
