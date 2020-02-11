import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-cache-tags',
    version='0.2',
    packages=find_packages(),
    description='Adds tagging to Django view caches',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nick Nelson',
    author_email='nick.eugene.nelson@gmail.com',
    url='https://github.com/nicknelson/django-cache-tags/',
    license='MIT',
    install_requires=[
        'Django>=2.0',
    ]
)
