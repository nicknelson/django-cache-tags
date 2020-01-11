from __future__ import unicode_literals

from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class DjangoCacheTagsConfig(AppConfig):
    name = 'django_cache_tags'


class AdminConfig(AdminConfig):
    default_site = 'django_cache_tags.admin.AdminSite'
