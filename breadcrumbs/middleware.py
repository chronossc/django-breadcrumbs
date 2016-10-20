# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import Http404
from .breadcrumbs import Breadcrumbs

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    # Works perfectly for everyone using MIDDLEWARE_CLASSES
    MiddlewareMixin = object


class BreadcrumbsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'breadcrumbs'):
            request.breadcrumbs = Breadcrumbs()


class FlatpageFallbackMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # do nothing if flatpages middleware isn't enabled, also if response
        # code isn't 404.
        if response.status_code != 404:
            return response
        try:
            from .views import flatpage
            return flatpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
