# -*- coding: utf-8 -*-

# TODO: Write unit tests!!!

# run this script on your shell
from breadcrumbs import Breadcrumbs

bds = Breadcrumbs()

# fill one per time
for i in range(5):
    bds('name%s' % i, 'url%s' % i)


# create a simple class to emulate one object with name and url
class EmulateObj(object):
    def __init__(self, *args):
        self.name = args[0]
        self.url = args[1]

# add 10 objects
bds([EmulateObj('name %s' % (i + 10), 'url %s' % (i + 10)) for i in range(10)])

# print all
for bd in bds:
    print bd.name, bd.url
