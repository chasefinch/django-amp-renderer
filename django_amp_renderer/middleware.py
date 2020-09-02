# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
import re
from builtins import bytes  # noqa
from builtins import str  # noqa

# Third Party
from amp_renderer import AMPRenderer

# Django
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import DjangoUnicodeDecodeError


class AMPRenderingMiddleware(MiddlewareMixin):
    # These will be passed along to AMP Renderer
    should_strip_comments = False
    should_trim_attrs = False

    def process_response(self, request, response):
        if not response.has_header('Content-Type') or 'text/html' not in response['Content-Type']:
            return response

        try:
            content = response.content.decode('utf-8').strip()
        except (DjangoUnicodeDecodeError, UnicodeDecodeError):
            pass
        else:
            """If the script is included in the document, then apply the
            transformations that the script would eventually happen on the
            client.

            Caveats:
                This only applies the middleware if AMP v0 is included directly
                from the https://cdn.ampproject.org/v0.(m?)js. If using RTVs or
                some other method, this won’t apply as written.

                This regex doesn’t check that quotes are balanced, or fully
                confirm that the import script is valid.
            """

            attribute_regexes = [
                r"""defer""",
                r"""async""",
                r"""type=['"]module['"]""",
            ]

            regex = \
                r"""<script({opt})*\s+src=['"]https://cdn\.ampproject\.org/(lts/)?v0\.m?js['"]""" \
                r"""({opt})*\s*>\s*</script>""".format(
                    opt='|'.join(r'\s+{}'.format(r) for r in attribute_regexes))

            if re.search(regex, content):
                boilerplate_header = 'Ignored'

                parser = AMPRenderer(
                    runtime_version=settings.AMP_RUNTIME_VERSION,
                    runtime_styles=settings.AMP_RUNTIME_STYLES)

                parser.should_strip_comments = self.should_strip_comments
                parser.should_trim_attrs = self.should_trim_attrs
                content = parser.render(content)

                response.content = content
                response['Content-Length'] = len(response.content)

                if parser.no_boilerplate:
                    boilerplate_header = 'Removed'

                """Set a header on the response for downstream code to know
                whether the boilerplate was removed."""
                response['Boilerplate-Status'] = boilerplate_header

        return response
