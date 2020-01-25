from django.middleware.cache import CacheMiddleware, UpdateCacheMiddleware, FetchFromCacheMiddleware
from django.utils.cache import learn_cache_key, get_max_age, has_vary_header, patch_response_headers
from django_cache_tags.utils import cache


class CustomUpdateCacheMiddleware(UpdateCacheMiddleware):

    def process_response(self, request, response):
        if request.COOKIES.get('view_uncached') == 'true' and request.user.is_authenticated:
            return response
        else:
            middleware_cache_tags = []

            if not self._should_update_cache(request, response):
                return response

            if response.streaming or response.status_code not in (200, 304):
                return response

            # Don't cache responses that set a user-specific (and maybe security
            # sensitive) cookie in response to a cookie-less request.
            if not request.COOKIES and response.cookies and has_vary_header(response, 'Cookie'):
                return response

            # Don't cache a response with 'Cache-Control: private'
            if 'private' in response.get('Cache-Control', ()):
                return response

            # Try to get the timeout from the "max-age" section of the "Cache-
            # Control" header before reverting to using the default cache_timeout
            # length.
            timeout = get_max_age(response)
            if timeout is None:
                timeout = self.cache_timeout
            elif timeout == 0:
                # max-age was set to 0, don't bother caching.
                return response
            patch_response_headers(response, timeout)
            if response.has_header('X-Additional-Cache-Tags'):
                middleware_cache_tags = response.__getitem__('X-Additional-Cache-Tags').split(",") + self.cache_tags
            if timeout and response.status_code == 200:
                cache_key = learn_cache_key(request, response, timeout, self.key_prefix, cache=self.cache)
                # add this cache_key to a cache_keys cache with tags

                cache.add_cache_key(request, cache_key, tags=middleware_cache_tags)

                if hasattr(response, 'render') and callable(response.render):
                    response.add_post_render_callback(
                        lambda r: self.cache.set(cache_key, r, timeout)
                    )
                else:
                    self.cache.set(cache_key, response, timeout)
            return response


class CustomFetchFromCacheMiddleware(FetchFromCacheMiddleware):
    def process_request(self, request):
        if request.COOKIES.get('view_uncached') == 'true' and request.user.is_authenticated:
            return None
        else:
            return FetchFromCacheMiddleware.process_request(self, request)


class CustomCacheMiddleware(CustomUpdateCacheMiddleware, CustomFetchFromCacheMiddleware):
    cache_tags = []

    def __init__(self, get_response=None, cache_timeout=None, **kwargs):
        try:
            view_tags = kwargs['tags']
            if view_tags is None:
                view_tags = []
        except KeyError:
            view_tags = []
        self.cache_tags = view_tags

        CacheMiddleware.__init__(self, get_response, cache_timeout, **kwargs)
