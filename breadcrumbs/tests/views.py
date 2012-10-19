# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

def page1(request):
    request.breadcrumbs("Page 1", request.get_full_path())
    return render_to_response('page1.html', {},
        context_instance=RequestContext(request))
