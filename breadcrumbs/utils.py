# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.cache import cache
from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404
from django.utils import importlib
from django.utils.decorators import classonlymethod

from .breadcrumbs import Breadcrumbs
from .exceptions import BreadcrumbsError, BreadcrumbsNotSet

logger = logging.getLogger('breadcrumbs')


def make_flatpages_cache_key():
    """
    Create a cache key based on some basic data, respecting defined site.
    """
    key = "flatpages_cache_%s-%s" % (hash(settings.SITE_ID),
                                     hash(settings.SECRET_KEY))

    return key


def get_flapage_from_cache(url):
    """
    Try get flatpage from cache entry with all flatpages by url.
    If not found, create cache and return flatpage from db.

    This probably avoid some hits on DB.
    """
    site_id = settings.SITE_ID
    cache_key = make_flatpages_cache_key()
    flatpages = cache.get(cache_key)
    if flatpages and url in flatpages:
        return flatpages[url]

    # flatpages cache not exist or flatpage not found.

    # 1. get all flatpages.
    flatpages = dict(
        [(f.url, f) for f in FlatPage.objects.filter(sites__id__exact=site_id)
                                             .order_by('url')]
    )

    # 2. if url not in flatpages, raise Http404
    if url not in flatpages:
        raise Http404

    # 3. if url in flatpages, recreate cache and return flatpage
    cache.delete(cache_key)
    cache.add(cache_key, flatpages)
    return flatpages[url]


def breadcrumbs_for_flatpages(request, flatpage):
    """ given request and flatpage instance create breadcrumbs for all flat
    pages """
    if not hasattr(request, 'breadcrumbs') or \
            not isinstance(request.breadcrumbs, Breadcrumbs):
        raise BreadcrumbsNotSet(u"You need to setup breadcrumbs to use this "
                                u"function.")

    if not isinstance(flatpage, FlatPage) or not hasattr(flatpage, 'id'):
        raise TypeError(u"flatpage argument isn't a FlatPage instance or not "
                        u"have id.")

    # URL for a flatpage can be composed of other flatpages, ex:
    #
    # We have:
    #   flatpage01 = /flat01/
    #   flatpage02 = /flat01/flat02/
    #   flatpage03 = /flat01/flat02/flat03/
    #
    # In breadcrumbs we want to know each title of each page, so we split url
    # in parts, and try to get flatpage title.
    #
    # However, you can define something like that in your urls.py:
    #   (r'^pages/', include('breadcrumbs.urls')),
    # And, we will never know what is /pages/, so we ignore it for now.
    paths = []
    for part in request.path_info.split(u"/"):
        # When split we have u"" for slashes
        if len(part) == 0:
            continue
        # Add slash agai
        if not part.startswith(u"/"):
            part = u"/" + part
        if not part.endswith(u"/"):
            part = part + u"/"
        # If we have something on paths, url for flatpage is composed of what
        # we have in path + part. Note that strings in path not have last
        # slash, but part have.
        if len(paths) > 0:
            url = u"".join(paths + [part])
        else:
            url = part
        # if part of url is same url of flatpage instance, we don't hit
        # database again, we get page from FlatPage instance.
        # If part of url isn't same url of flatpage instance, we try to get it.
        # If page doesn't exist, we just continue to next part.
        if url == flatpage.url:
            request.breadcrumbs(flatpage.title, flatpage.url)
        else:
            try:
                f = FlatPage.objects.get(url=url, sites=settings.SITE_ID)
            except FlatPage.DoesNotExist:
                # TODO: this part can be a view, maybe is a good idea get that
                # view and check for viewfunc.breadcrumb_title or
                # viewclass.breadcrumb_title attributes.
                continue
            else:
                request.breadcrumbs(f.title, f.url)
        # add last part of path in paths with one slash
        paths.append(u"/" + url[1:-1].rpartition(u"/")[-1])


def get_object(module_name, obj_name):
    """
    Get the object based on module and name
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise ImportError('Invalid object path: %s' % module_name)

    try:
        obj = getattr(module, obj_name)
    except AttributeError:
        raise ImportError('Invalid object name: %s' % obj_name)
    else:
        return obj


class BreadcrumbMixin(object):

    """
    This is a mixin to use with any class based view. To use it just add the
    `View.title` attribute or `View.get_view_title` method wich should return
    the view title.

    The URL will come from `View.get_absolute_url` method.

    The mixin will call the `View.register_breadcrumb` before rendering, so you
    can change this method also if need something more complex.
    """
    title = None

    @classmethod
    def register_breadcrumb(cls, url, breadcrumbs, *args, **kwargs):
        if not cls.title:
            raise BreadcrumbsError(
                "You must set a attribute title when using BreadcrumbsMixin."
            )
        # import ipdb; ipdb.set_trace()
        breadcrumbs(cls.title, url)

    def render_to_response(self, context, **response_kwargs):
        build_breadcrumbs(self)
        return super(BreadcrumbMixin, self)\
            .render_to_response(context, **response_kwargs)

    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super(BreadcrumbMixin, cls).as_view(**initkwargs)
        view.cls = cls
        return view


def build_breadcrumbs(view):
    parts = view.request.path.split('/')
    url_parts = []
    for url_part in parts:
        url_parts.append(url_part)
        url = '/'.join(url_parts)

        if not url.startswith('/'):
            url = '/' + url
        if not url.endswith('/'):
            url = url + '/'

        if view.request.path == url:
            logger.debug("Url '%s' match to '%s'.", url, view)
            view.register_breadcrumb(
                url, view.request.breadcrumbs, *view.args, **view.kwargs
            )
            break
        else:
            try:
                match = resolve(url)
            except Resolver404:
                logger.debug("Url '%s' does not exist.", url)
                continue
            else:
                logger.debug("Url '%s' match to '%s'.", url, match)
                try:
                    match.func.cls.register_breadcrumb(
                        url, view.request.breadcrumbs,
                        *match.args, **match.kwargs
                    )
                except AttributeError:
                    if hasattr(match.func, 'title'):
                        view.request.breadcrumbs(match.func.title, url)
