from django.contrib import admin, messages
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import path


class AdminSite(admin.AdminSite):
    def break_site_cache(self, request):
        '''
          A shortcut to clear all caches
        '''
        cache.clear()
        messages.add_message(request, messages.SUCCESS, 'All caches cleared!')
        return HttpResponseRedirect('/admin/')

    def view_site_uncached(self, request):
        '''
          Sets a "view_uncached" cookie that bypasses loading the
          cached version of a page. This also includes a toolbar
          to easily flip back and forth between cached and uncached
          views. To include this in your templates, pass the cookie
          to the context on your view, such as:
          ```
            def get_context_data(self, **kwargs):
              if self.request.user.is_authenticated and self.request.COOKIES.get('view_uncached') == 'true':
                context['view_uncached'] = self.request.COOKIES.get('view_uncached')
          ```
          And then include this in your template:
          ```
            {% if view_uncached == "true" %}
              {% include 'components/admin-bar.html' %}
            {% endif %}
          ```
        '''
        redirect = request.GET.get('return') if request.GET.get('return') else '/'
        response = HttpResponseRedirect(redirect)
        response.set_cookie('view_uncached', 'true')
        return response

    def remove_uncache_cookie(self, request):
        redirect = request.GET.get('return') if request.GET.get('return') else '/'
        response = HttpResponseRedirect(redirect)
        response.delete_cookie('view_uncached')
        return response

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('break_site_cache/', self.admin_view(self.break_site_cache), name='attractions_break_site_cache'),
            path('view_site_uncached/', self.admin_view(self.view_site_uncached), name='attractions_view_site_uncached'),
            path('remove_uncache_cookie/', self.admin_view(self.remove_uncache_cookie), name='attractions_remove_uncache_cookie'),
        ]
        return my_urls + urls
