from django_cache_tags.utils.cache import cache_view
from django.views.generic.base import TemplateView


@cache_view
class TestView(TemplateView):
    cache_tags = ['test_tag']
    pass
