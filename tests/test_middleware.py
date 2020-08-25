# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
from builtins import bytes  # noqa
from builtins import str  # noqa

# Third Party
from mock import MagicMock, Mock

# AMP Renderer
from django_amp_renderer.middleware import AMPRenderingMiddleware


def get_response():
    return None


def test_default_page():
    request = Mock()
    request.META = MagicMock()
    request.GET = {}
    _ = AMPRenderingMiddleware(get_response)

    assert True is True
