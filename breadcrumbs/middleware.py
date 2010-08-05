# -*- coding: utf-8 -*-
from .breadcrumbs import Breadcrumbs
from .utils import breadcrumbs_for_flatpages
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.views import flatpage
from django.http import Http404
from django.shortcuts import get_object_or_404

class BreadcrumbsMiddleware(object):

    def process_request(self,request):
        request.breadcrumbs = Breadcrumbs()
        request.breadcrumbs._clean()
        return None

class FlatpageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response # No need to check for a flatpage for non-404 responses.
        try:
            # In old 1.0 we have a patch for flat pages, but as live app, we can't
            # touch in django code, so we clone flat page middleware with some
            # modifications :)
            # We need to get flat page, aniway, but if fail, fail silently. Also we
            # check for permissions, parts of code are from flat page view
            f = get_object_or_404(FlatPage, url__exact=request.path_info, sites__id__exact=settings.SITE_ID)
            if f: breadcrumbs_for_flatpages(request,f)
            return flatpage(request, request.path_info)
        # Return the original response if any errors happened. Because this
        # is a middleware, we can't assume the errors will be caught elsewhere.
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
