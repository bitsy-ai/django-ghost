#!/usr/bin/env python
import os
from typing import List

from setuptools import setup, find_namespace_packages
from django_ghost import __version__

long_description: str = open(
    os.path.join(os.path.dirname(__file__), "README.md")
).read()
install_requires = ["django>=3.2,<4", "psycopg2", "requests>=2.28", "PyJWT>=2.6"]

python_requires = ">3.7"

setup(
    name="django_ghost",
    version=__version__,
    packages=find_namespace_packages(exclude=["test", "tests", "config"]),
    author="Leigh Johnson",
    author_email="leigh@bitsy.ai",
    description="Django Ghost is a Django app to sync a Django model with Ghost CMS newsletter subscribers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="django ghost cms",
    url="http://github.com/bitsy-ai/django-ghost",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
    ],
    zip_safe=True,
    install_requires=install_requires,
    test_suite="pytest",
    python_requires=python_requires,
    include_package_data=True,
)
