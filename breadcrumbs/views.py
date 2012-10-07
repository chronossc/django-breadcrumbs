from django.conf import settings
from django.contrib.flatpages.views import render_flatpage
from django.http import Http404, HttpResponsePermanentRedirect
from utils import breadcrumbs_for_flatpages, get_flapage_from_cache


def flatpage(request, url):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """

    if not url.startswith('/'):
        url = '/' + url
    try:
        # try load flatpage from cache, else, update cache and get from DB
        f = get_flapage_from_cache(url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_flapage_from_cache(url)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise

    # create breadcrumbs
    breadcrumbs_for_flatpages(request, f)

    return render_flatpage(request, f)
