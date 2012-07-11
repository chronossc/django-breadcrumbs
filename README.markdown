*django-breadcrumbs* is a breadcrumb system to Django framework that allow you to add custom breadcrumbs for simple views, generic views and support Django FlatPages app.

In format of a pluggable middleware that add a breadcrumbs callable/iterable in your request object, allowing you to set  breadcrumbs (one or more) in each view accepting objects, lists or tuples added from request.breadcrumbs and is iterable, easy to use in templates providing a object with name and url attributes.

*Note: For Django 1.x, check for tag 1.0 and patches :)*

#1 - Install django-breadcrumbs

Just put in your python path and add **breadcrumbs.middleware.BreadcrumbsMiddleware** to your **MIDDLEWARE_CLASSES**.
Also, if you did't put request context processor on yours TEMPLATE_CONTEXT_PROCESSORS, add it, ex:

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.contrib.messages.context_processors.messages",
        'django.core.context_processors.request',
    )

#2 - Adding breadcrumbs

To add breadcrumbs you just need to call **request.breadcrumbs('Title',url)**, ex:

	def about(request):
		request.breadcrumbs(_("About"),request.path_info)
		...

	def generic_crud_view(request,model,action):
		"""
		model = model name
		action = action name
		"""

		request.breadcrumbs([
			(_(model.title()),'/crud/%s' % model),
			(_('%s %s') % (action.title(),model.title()),'/crud/%s/%s' % (model,action)),
		])

		...

All modes of add a breadcrumb:

	# one by one
	request.breadcrumbs( name, url )

	# various tuples/lists
	request.breadcrumbs( ( (name1, url1), (name2, url2), (name3, url3), ...,) )
	request.breadcrumbs( [ [name1, url1], [name2, url2], [name3, url3], ...] )

	# objects with attributes name and url in list / tuple format:
	request.breadcrumbs( ( obj1, obj2, obj3, obj4, ......) )
	request.breadcrumbs( [ obj1, obj2, obj3, obj4, ......] )

*Note: You can use request.breadcrumbs safely in any middleware after BreadcrumbsMiddleware or any place where  you have request object after BreadcrumbsMiddleware are processed*

#3 - Enable FlatPages + Breadcrumbs

FlatPages is a app that allow user create urls with static content and a title. But create breadcrumbs for this kind of 'unknow' url path isn't fun at all, so I modified FlatpageFallbackMiddleware to fill breadcrumbs for each flat page in path.

Is really easy to use, just add **breadcrumbs.middleware.FlatpageFallbackMiddleware** in your **MIDDLEWARE_CLASSES** after BreadcrumbsMiddleware and all done!

#4 - Using in templates

To use breadcrumbs in template, only that you need is iterate over breadcrumbs, example:

	{% for breadcrumb in request.breadcrumbs %}
	<a href="{{ breadcrumb.url }}">{{ breadcrumb.name }}</a>{% if not forloop.last %} &raquo; {% endif %}
	{% endfor %}

#5 - Options

django-breadcrumbs have a single option to set in your settings.py:

	BREADCRUMBS_AUTO_HOME: defaults to False, If True, breadcrumbs add as first Breadcrumb in list (_("Home"),u"/")
	BREADCRUMBS_HOME_TITLE: defaults to _(u'Home')

