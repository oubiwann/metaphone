from setuptools import setup, find_packages
import io

from metaphone import meta


setup(
    name=meta.display_name,
    version=meta.version,
    description=meta.description,
    author=meta.author,
    author_email=meta.author_email,
    url=meta.url,
    license=meta.license,
    packages=find_packages(),
    long_description=io.open("README.rst", encoding='utf-8').read(),
    tests_require = ['nose'],
    test_suite = 'nose.collector',
    )
