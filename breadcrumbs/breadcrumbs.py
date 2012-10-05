"""
Classes to add request.breadcrumbs as one class to have a list of breadcrumbs
TODO: maybe is better to move to contrib/breadcrumbs
"""

from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class Singleton(object):
    """
    We use a simple singleton pattern in Breadcrumbs.
    Example from http://svn.ademar.org/code/trunk/junk-code/singleton_vs_borg.py
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it._1st_init(*args, **kwds)
        return it

    def _1st_init(self, *args, **kwds):
        pass


class BreadcrumbsInvalidFormat(Exception):
    """
    Simple exception that can be extended
    """
    pass


class BreadcrumbsNotSet(Exception):
    """
    Raised in utils.breadcrumbs_for_flatpages when we not have breadcrumbs in
    request.
    """
    pass


class Breadcrumb(object):
    """
    Breadcrumb can have methods to customize breadcrumb object, Breadcrumbs
    class send to us name and url.
    """
    def __init__(self, name, url):
        # HERE
        #
        # If I don't use force_unicode, always runs ok, but have problems on
        # template with unicode text
        self.name = name
        self.url = url

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s,%s" % (self.name, self.url)

    def __repr__(self):
        return u"Breadcrumb <%s,%s>" % (self.name, self.url)


class Breadcrumbs(Singleton):
    """
    Breadcrumbs maintain a list of breadcrumbs that you can get interating with
    class or with get_breadcrumbs().
    """
    def _1st_init(self, *args, **kwargs):
        """
        singleton function that start some variables
        """
        self._clean()
        self.__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if not len(args) and not len(kwargs):
            return self
        return self.__init__(*args, **kwargs)

    def __fill_home(self):
        # fill home if settings.BREADCRUMBS_AUTO_HOME is True
        if self.__autohome and len(self.__bds) == 0:
            home_title = getattr(settings, 'BREADCRUMBS_HOME_TITLE', _(u'Home'))
            self.__fill_bds((home_title, u"/"))

    def _clean(self):
        self.__bds = []
        self.__autohome = getattr(settings, 'BREADCRUMBS_AUTO_HOME', False)
        self.__urls = []
        self.__fill_home()

    def __init__(self, *args, **kwargs):
        """
        Call validate and if ok, call fill bd
        """
        # match Breadcrumbs( 'name', 'url' )
        if len(args) == 2 and type(args[0]) not in (list, tuple):
            if(self.__validate(args, 0)):
                self.__fill_bds(args)
        # match ( ( 'name', 'url'), ..) and samething with list
        elif len(args) == 1 and type(args[0]) in (list, tuple) \
                and len(args[0]) > 0:
            for i, arg in enumerate(args[0]):
                if self.__validate(arg, i):
                    self.__fill_bds(arg)
        # try to ( obj1, obj2, ... ) and samething with list
        else:
            for i, arg in enumerate(args):
                if(self.__validate(arg, i)):
                    self.__fill_bds(arg)

    def __validate(self, obj, index):
        """
        check for object type and return a string as name for each item of a
        list or tuple with items, if error was found raise
        BreadcrumbsInvalidFormat
        """
        # for list or tuple
        if type(obj) in (list, tuple):
            if len(obj) == 2:
                if (not obj[0] and not obj[1]) or \
                        (type(obj[0]) not in (str, unicode) and \
                        type(obj[1]) not in (str, unicode)):
                    raise BreadcrumbsInvalidFormat(u"Invalid format for \
                        breadcrumb %s in %s" % (index, type(obj).__name__))
            if len(obj) != 2:
                raise BreadcrumbsInvalidFormat(
                    u"Wrong itens number in breadcrumb %s in %s. \
                    You need to send as example (name,url)" % \
                    (index, type(obj).__name__)
                )
        # for objects
        elif not hasattr(obj, 'name') and not hasattr(obj, 'url'):
            raise BreadcrumbsInvalidFormat(u"You need to use a tuple like "
                "(name,url) or object with name and url attributes for "
                "breadcrumb.")
        return True

    def __fill_bds(self, bd):
        """
        simple interface to add Breadcrumb to bds
        """
        if hasattr(bd, 'name') and hasattr(bd, 'url'):
            bd = Breadcrumb(bd.name, bd.url)
        else:
            bd = Breadcrumb(*bd)
        if bd.url not in self.__urls:
            self.__bds.append(bd)
            self.__urls.append(bd.url)

    def __iter__(self):
        return iter(self.__bds)

    def __getitem__(self, key):
        return self.__bds[key]

    def __repr__(self):
        return self.__unicode__()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"Breadcrumbs <%s>" % u", ".join([mark_safe(item.name) for item \
                                                    in self[:10]] + [u' ...'])

    def all(self):
        return self.__bds

# vim: ts=4 sts=4 sw=4 et ai
