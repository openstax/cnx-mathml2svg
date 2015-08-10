# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
from pyramid.config import Configurator
from pyramid.response import Response

__all__ = ('main',)


def convert(request):
    """Convert the POST'd MathML to SVG"""
    return Response()


def main(global_config, **settings):
    """Application factory"""
    config = Configurator(settings=settings)
    config.add_route('convert', '/', request_method='POST')
    config.add_view(convert, route_name='convert')
    return config.make_wsgi_app()
