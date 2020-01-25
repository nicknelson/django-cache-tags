from django.test import TestCase, RequestFactory
from django.urls import reverse
from django_cache_tags.views import TestView
from django_cache_tags.utils import cache


class CacheTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_view_cache(self):
        # test_url = reverse('test-view')
        request = self.factory.get('/test')
        response = TestView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_cache_headers(self):
        pass

    def test_cache_break(self):
        cache.break_cache_by_tag(['/test', 'test_tag'])
