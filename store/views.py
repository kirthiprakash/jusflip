import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template import loader
from haystack.query import SearchQuerySet
from django.db.models import Count
import logging

# Create your views here.


from django.views.generic import View

from store.models import Product
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ProductView(View):
    """
    GET method lists products. Filters by category, brand, price and stock status.
    Supports pagination
    """

    def get(self, request):

        page_str = request.GET.get("page", 1)  # default page: 1
        items_per_page = request.GET.get("items_per_page", 24)  # default items per page: 18
        brand_list = request.GET.getlist("brand")
        category_list = request.GET.getlist('category')
        price_range_low_str = request.GET.getlist('price_range_low')
        price_range_high_str = request.GET.getlist('price_range_high')
        is_in_stock_str = request.GET.get('is_in_stock', "false")
        is_in_stock = True if "true" == is_in_stock_str else False

        try:
            page = int(page_str)
            product_qs = Product.objects.filter()
            if brand_list:
                product_qs = product_qs.filter(brand__in=brand_list)
            if category_list:
                product_qs = product_qs.filter(category__in=category_list)
            if is_in_stock:
                product_qs = product_qs.filter(stock="In Stock")
            if price_range_low_str:
                try:
                    price_range_low = min([float(el) for el in price_range_low_str])
                    print price_range_low
                    product_qs = product_qs.filter(available_price__gte=price_range_low)
                except ValueError as e:
                    raise ValidationError("Invalid price_range_low: {}".format(price_range_low_str))
            if price_range_high_str:
                try:
                    price_range_high = max([float(el) for el in price_range_high_str])
                    print price_range_high
                    product_qs = product_qs.filter(available_price__lte=price_range_high)
                except ValueError as e:
                    raise ValidationError("Invalid price_range_high: {}".format(price_range_high_str))

            paginator = Paginator(product_qs, items_per_page)
            query_path = request.GET.urlencode()
            page_information = {
                "next_page": "/store/product/?page={}&{}".format(min(paginator.num_pages, page + 1), query_path),
                "previous_page": "/store/product/?page={}&{}".format(max(1, page - 1), query_path)}
            try:
                products = paginator.page(page)
            except PageNotAnInteger:
                products = paginator.page(1)
            except EmptyPage:
                products = paginator.page(paginator.num_pages)

            product_json = serializers.serialize("json", products, fields=Product.SERIALIZATION_FIELDS)
            products = json.loads(product_json)
            response_obj = {"products": products, "page_info": page_information}
            response = json.dumps(response_obj)
            return HttpResponse(response)
        except ValidationError as e:
            logging.exception(e)
            bad_request_response_obj = {"message": e.message}
            bad_request_response = json.dumps(bad_request_response_obj)
            return HttpResponse(bad_request_response, status=400)
        except Exception as e:
            logging.exception(e)
            bad_request_response_obj = {"message": "Something went wrong. Contact the Administrator"}
            bad_request_response = json.dumps(bad_request_response_obj)
            return HttpResponse(bad_request_response, status=500)


class SearchView(View):
    """
    GET method does a search on every attribute of the product, be it brand name, category or any features related to
    products. Supports pagination.

    """

    def get(self, request):
        search_key = request.GET.get("q", "")
        page_str = request.GET.get("page", 1)  # default page: 1
        items_per_page = request.GET.get("items_per_page", 24)  # default items per page: 10
        try:
            page = int(page_str)
            # Queries the search backend (ElasticSearch) for the relevant keyword
            search_qs = SearchQuerySet().filter(content=search_key)
            paginator = Paginator(search_qs, items_per_page)
            page_information = {
                "next_page": "/store/product/search/?q={}&page={}".format(search_key,
                                                                          min(paginator.num_pages, page + 1)),
                "previous_page": "/store/product/search/?q={}&page={}".format(search_key, max(1, page - 1))}
            try:
                product_sqs = paginator.page(page)
            except PageNotAnInteger:
                products_sqs = paginator.page(1)
            except EmptyPage:
                products_sqs = paginator.page(paginator.num_pages)
            except Exception as e:
                return
            products = self.search_to_model_queryset_gen(product_sqs)
            product_json = serializers.serialize('json', products, fields=Product.SERIALIZATION_FIELDS)
            products = json.loads(product_json)
            response_obj = {"products": products, "page_info": page_information}
            response = json.dumps(response_obj)
            return HttpResponse(response)
        except Exception as e:
            logging.exception(e)
            bad_request_response_obj = {"message": "Something went wrong. Contact the Administrator"}
            bad_request_response = json.dumps(bad_request_response_obj)
            return HttpResponse(bad_request_response, status=500)

    def search_to_model_queryset_gen(self, search_qs):
        """
        Converts HayStack's SearchQuerySet type to Django's model generator
        :param search_qs: HayStack's SearchQuerySet
        :return: => Generator
        """
        for item in search_qs:
            yield item.object


class FilterOptionView(View):
    def get(self, request):
        product_categories = Product.objects.all().values('category').distinct().order_by('category')[0:50]
        brand_categories = Product.objects.all().values('brand').distinct().order_by('brand')[0:200]
        response_obj = {}
        response_obj['categories'] = list(product_categories)
        response_obj['brands'] = list(brand_categories)
        response = json.dumps(response_obj)
        return HttpResponse(response)


def index(request):
    try:
        template = loader.get_template('store/index.html')
        return HttpResponse(template.render({}, request))
    except Exception as e:
        logging.exception(e)
        bad_request_response_obj = {"message": "Something went wrong. Contact the Administrator"}
        bad_request_response = json.dumps(bad_request_response_obj)
        return HttpResponse(bad_request_response, status=500)
