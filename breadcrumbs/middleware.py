# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import Http404
from breadcrumbs import Breadcrumbs
from views import flatpage


class BreadcrumbsMiddleware(object):

    def process_request(self, request):
        request.breadcrumbs = Breadcrumbs()
        request.breadcrumbs._clean()


class FlatpageFallbackMiddleware(object):
    def process_response(self, request, response):
        # do nothing if flatpages middleware isn't enabled, also if response
        # code isn't 404.
        if response.status_code != 404:
            return response
        try:
            return flatpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
