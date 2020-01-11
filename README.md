# django-cache-tags

django-cache-tags adds some useful cache setting and breaking functions to Django's built-in view caching, namely the ability to add arbitrary tags to caches.

It will:
- Automatically tag cached views with the view path that created the cache, so you only need to knew the url path to break all related views.
- Allow you to add any arbitrary tag strings to a view, letting you break groups of related pages.
- Easily set specific methods you want to cache in a view without having to define those methods.

## Installation

Install django-cache-tags with pip:
```
    pip install django-cache-tags
```

Include it in your `INSTALLED_APPS` in settings:
```
    INSTALLED_APPS = [
        ...
        'django_cache_tags'
    ]
```

Use the new `@cache_view` decorator in your [Django class-based views](https://docs.djangoproject.com/en/3.0/topics/class-based-views/), with any of the provided optional class arguments:
```
    from django_cache_tags.utils.cache import cache_view

    @cache_view
    class MyDetailPage(TemplateView):
        cache_tags = ['my', 'detail', 'page']
        cache_methods = ['list', 'retrieve', 'get']
        cache_timeout = 60 * 60 * 24
```

Possible arguments:
- `cache_methods`: A list of methods (list, retrieve) to cache for the view
- `cache_timeout`: How long to cache the page for, in seconds. Use `None` to cache indefinitely, or `0` to never cache
- `cache_tags`: A list of strings to tag the caches with
- `cache_alias`: The name of the cache to use (if not the default), defined in settings
- `key_prefix`: A prefix to prepend to cache keys

You can then break caches with the `break_cache_by_tag` method:
```
    from django_cache_tags.utils.cache import break_cache_by_tag

    break_cache_by_tag('detail')
    break_cache_by_tag('/my/page/path')
    break_cache_by_tag(['list', 'of', 'tags', '/or/paths'])
```


