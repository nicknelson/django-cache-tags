from django_cache_tags.middleware.cache import CustomCacheMiddleware
from django.core.cache import cache
from django.utils.decorators import method_decorator, decorator_from_middleware_with_args
from copy import copy


def add_cache_key(request, cache_key, tags=[]):
    tag_list = copy(tags)
    # add key to path tag
    tag_list.append(request.path)

    # add key to each tag set
    for tag in tag_list:
        tag_cache_key_name = f'cache_keys:{tag}'
        tag_cache_keys = cache.get(tag_cache_key_name) if cache.get(tag_cache_key_name) else set()
        tag_cache_keys.add(cache_key)
        cache.set(tag_cache_key_name, tag_cache_keys, None)

    # add tags to key set
    cache_key_tags_name = f'cache_tags:{cache_key}'
    cache_key_tags = cache.get(cache_key_tags_name).union(set(tag_list)) if cache.get(cache_key_tags_name) else set(tag_list)
    cache.set(cache_key_tags_name, cache_key_tags, None)

    tag_list = []


def break_cache_by_tag(tags):
    if type(tags) == str:
        tags = [tags]
    for tag in tags:
        tag_cache_keys = cache.get(f'cache_keys:{tag}')
        if tag_cache_keys:
            for key in tag_cache_keys:
                cache.delete(key)
                # print('deleted cache ', key)
                key_tags = cache.get(f'cache_tags:{key}')
                if key_tags:
                    for kt in key_tags:
                        if kt != tag:
                            these_keys = cache.get(f'cache_keys:{kt}')
                            if these_keys:
                                try:
                                    kt_keys = these_keys.remove(key)
                                except KeyError:
                                    # cache key already removed from set
                                    kt_keys = these_keys
                                cache.set(f'cache_keys:{kt}', kt_keys, None)
                cache.delete(f'cache_tags:{key}')
            cache.delete(f'cache_keys:{tag}')
        else:
            # print('no cache key found for', tag)
            pass


def cache_page(timeout, *, cache=None, key_prefix=None, tags=[]):
    # overriding @cache_page decorator to use custom middleware and accept tags
    return decorator_from_middleware_with_args(CustomCacheMiddleware)(
        cache_timeout=timeout, cache_alias=cache, key_prefix=key_prefix, tags=tags
    )


def cache_view(view):
    '''
    Decorator function to be used on View and Viewset classes
    Doesn't take any parameters, instead it uses the following class arguments:
        cache_methods = A list of methods (list, retrieve) to cache for the view
        cache_timeout = How long to cache the page for, in seconds
                        Use `None` to cache indefinitely, or `0` to never cache
        cache_tags = A list of strings to tag the caches with
        cache_alias = The name of the cache to use (if not the default), defined in settings
        key_prefix = A prefix to prepend to cache keys
    '''
    cache_methods = view.cache_methods if hasattr(view, "cache_methods") else ['list', 'retrieve', 'get']
    timeout = view.cache_timeout if hasattr(view, "cache_timeout") else 60 * 60 * 24
    cache = view.cache_alias if hasattr(view, "cache_alias") else None
    key_prefix = view.key_prefix if hasattr(view, "key_prefix") else None
    tags = view.cache_tags if hasattr(view, "cache_tags") else []

    for name, method in view.__dict__.items():
        if name in cache_methods:
            @method_decorator(cache_page(timeout, cache=cache, key_prefix=key_prefix, tags=tags))
            def cached_method(self, request, *args, original_method=method, **kwargs):
                return original_method(self, request, *args, **kwargs)

            exec(f'view.{name} = cached_method')

    return view
