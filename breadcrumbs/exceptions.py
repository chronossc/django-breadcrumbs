# -*- coding: UTF-8 -*-


class BreadcrumbsError(Exception):
    """
    Generic error for breadcrumbs app.
    """
    pass


class BreadcrumbsInvalidFormat(BreadcrumbsError):
    """
    TODO: shit of description.. check what this really does
    Simple exception that can be extended
    """
    pass


class BreadcrumbsNotSet(BreadcrumbsError):
    """
    Raised when we not have breadcrumbs in request.
    """
    pass
