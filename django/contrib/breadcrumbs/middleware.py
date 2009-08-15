from breadcrumbs import Breadcrumbs

class BreadcrumbsMiddleware(object):

    def process_request(self,request):
        request.breadcrumbs = Breadcrumbs()
        request.breadcrumbs._clean()
