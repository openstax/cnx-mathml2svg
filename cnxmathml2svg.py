# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2015, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
from pyramid.config import Configurator


__all__ = ('main',)


def main(global_config, **settings):
    """Application factory"""
    config = Configurator(settings=settings)
    return config.make_wsgi_app()
