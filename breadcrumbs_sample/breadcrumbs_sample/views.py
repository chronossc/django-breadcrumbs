
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic import TemplateView
from breadcrumbs.utils import BreadcrumbMixin


def home(request):
    return render_to_response(
        'home.html', {'text': 'Hello, this is home!'},
        context_instance=RequestContext(request))

home.title = 'site home'


def someview(request):
    request.breadcrumbs('just a view to show some url', request.path)

    return render_to_response(
        'home.html', {'text': 'Hello, this is some second view'},
        context_instance=RequestContext(request))


# CBVs
class CBVHome(BreadcrumbMixin, TemplateView):
    template_name = 'home.html'
    title = 'CBV Home'

    def get_context_data(self, **context):
        context = super(CBVHome, self).get_context_data(**context)
        context['text'] = "This is " + self.title
        return context


class CBVLevel1(BreadcrumbMixin, TemplateView):
    template_name = 'home.html'
    title = 'Level 1'

    def get_context_data(self, **context):
        context = super(CBVLevel1, self).get_context_data(**context)
        context['text'] = "This is " + self.title
        return context


class CBVLevel2WithArgs(BreadcrumbMixin, TemplateView):
    template_name = 'home.html'
    title = 'Level 2 with args'

    def get_context_data(self, **context):
        context = super(CBVLevel2WithArgs, self).get_context_data(**context)
        context['text'] = "This is " + self.title
        return context
