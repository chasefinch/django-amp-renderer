# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
from builtins import bytes  # noqa
from builtins import str  # noqa

# Third Party
from amp_renderer import AMPRenderer

# Django
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import DjangoUnicodeDecodeError


class AMPRenderingMiddleware(MiddlewareMixin):
    should_strip_comments = False
    should_trim_attrs = False

    def process_response(self, request, response):
        if not response.has_header('Content-Type') or 'text/html' not in response['Content-Type']:
            return response

        try:
            content = response.content.decode('utf-8').strip()
        except DjangoUnicodeDecodeError:
            pass
        else:
            parser = AMPRenderer(
                runtime_version=settings.AMP_RUNTIME_VERSION,
                runtime_styles=settings.AMP_RUNTIME_STYLES)

            parser.should_strip_comments = self.should_strip_comments
            parser.should_trim_attrs = self.should_trim_attrs
            content = parser.render(content)

            response.content = content
            response['Content-Length'] = len(response.content)

        return response
