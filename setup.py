# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup


IS_PY3 = sys.version_info > (3,)

install_requires = (
    'lxml',
    'pyramid',
    )
tests_require = [
    ]
extras_require = {
    'test': tests_require,
    }

description = "Simple webapp for transforming MathML to SVG"
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as readme:
    README = readme.read()
with open(os.path.join(here, 'CHANGES.rst')) as changes:
    CHANGELOG = changes.read()
changelog_header = """\
Change Log
==========
"""
long_description = '\n\n'.join([README, changelog_header, CHANGELOG])


setup(
    name='cnx-mathml2svg',
    version='1.0.0',
    author='Connexions team',
    author_email='info@cnx.org',
    url="https://github.com/connexions/cnx-mathml2svg",
    license='AGPL, See also LICENSE.txt',
    description=description,
    long_description=long_description,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    include_package_data=True,
    py_modules=['cnxmathml2svg'],
    test_suite='tests',
#    test_suite='tests.Test_Saxon.test_transform_failure_4',
    entry_points="""\
    [paste.app_factory]
    main = cnxmathml2svg:main
    """,
    )
