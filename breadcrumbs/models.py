# -*- coding: utf-8 -*-
from django.contrib.flatpages.models import FlatPage
from django.core.cache import cache
from django.db.models.signals import post_save
from utils import make_flatpages_cache_key


def clean_flatpages_cache(sender, **kw):
    """
    Invalidate flatpages cache, because some flatpage was saved!
    """
    cache.delete(make_flatpages_cache_key())

post_save.connect(clean_flatpages_cache, sender=FlatPage)
