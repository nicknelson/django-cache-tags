import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-cache-tags',
    version='0.1',
    packages=['django_cache_tags'],
    description='Adds tagging to Djagno view caches',
    long_description=README,
    author='Nick Nelson',
    author_email='whoisnicknelson@gmail.com',
    url='https://github.com/nicknelson/django-cache-tags/',
    license='MIT',
    install_requires=[
        'Django>=2.0',
    ]
)
