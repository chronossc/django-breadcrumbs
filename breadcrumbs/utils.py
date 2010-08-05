# -*- coding: utf-8 -*-
from .breadcrumbs import Breadcrumbs,BreadcrumbsNotSet
from django.contrib.flatpages.models import FlatPage
from django.http import Http404

def breadcrumbs_for_flatpages(request,flatpage):
    """ given request and flatpage instance create breadcrumbs for all flat
    pages """
    if not hasattr(request,'breadcrumbs') or \
        not isinstance(request.breadcrumbs,Breadcrumbs):
        raise BreadcrumbNotSet(u"You need to setup breadcrumbs to use this " + \
                "function.")

    if not isinstance(flatpage,FlatPage) or \
        not hasattr(flatpage,'id'):
        raise TypeError(u"flatpage argument isn't a FlatPage instance or " + \
            "not have id.")

    paths = []
    for part in request.path_info.split(u"/"):
        # When split we have u"" for slashes
        if len(part) == 0:
            continue
        # Add slash again
        if not part.startswith(u"/"):
            part = u"/"+part
        if not part.endswith(u"/"):
            part = part+u"/"
        # If we have something on paths, url for flatpage is composed of what we
        # have in path + part. Note that strins in path not have last slash, but
        # part have.
        if len(paths) > 0:
            url = u"".join(paths+[part])
        else:
            url = part
        # if is same url we don't hit database again
        # else, get page from FlatPage. If page doesn't exist, we allow raise
        # 404 because it is a url design problem, not flatpages or breadcrumbs
        # problem.
        if url == flatpage.url:
            request.breadcrumbs(flatpage.title,flatpage.url)
        else:
            try:
                f = FlatPage.objects.get(url=url)
            except FlatPage.DoesNotExist:
                raise Http404
            else:
                request.breadcrumbs(f.title,f.url)
        # add last part of path in paths with one slash
        paths.append(u"/"+url[1:-1].rpartition(u"/")[-1])

