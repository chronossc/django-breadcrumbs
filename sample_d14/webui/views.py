from django.shortcuts import render_to_response
from django.template.context import RequestContext


def home(request):
    return render_to_response('home.html',
        {'text': 'Hello, this is home!'},
        context_instance=RequestContext(request))


def someview(request):
    request.breadcrumbs('just a view to show some url', request.path)

    return render_to_response('home.html',
        {'text': 'Hello, this is some second view'},
        context_instance=RequestContext(request))
