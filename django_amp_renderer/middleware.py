"""Define middleware for applying AMPRenderer to the output of Django views."""

# Standard Library
import re

# Third Party
from amp_renderer import AMPRenderer

# Django
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils.encoding import DjangoUnicodeDecodeError


class AMPRenderingMiddleware(MiddlewareMixin):
    """Apply AMPRenderer to the output of Django views."""

    # These will be passed along to AMP Renderer
    should_strip_comments = False
    should_trim_attrs = False

    def process_response(self, request, response):
        """Process the response after the view has rendered it."""
        if not response.has_header("Content-Type") or "text/html" not in response["Content-Type"]:
            return response

        try:
            response_content = response.content.decode("utf-8").strip()
        except (DjangoUnicodeDecodeError, UnicodeDecodeError):
            return response

        # If the script is included in the document, then apply the
        # transformations that the script would eventually happen on the
        # client.

        # Caveats:
        #   - This only applies the middleware if AMP v0 is included directly
        #     from the https://cdn.ampproject.org/v0.(m?)js.
        #   - If using RTVs or some other method, this won’t apply as written.
        #   - This regex doesn’t check that quotes are balanced, or fully
        #     confirm that the import script is valid.

        attribute_patterns = [
            "defer",
            "async",
            "type=['\"]?module['\"]?",
            "crossorigin(=['\"]?anonymous['\"]?)?",
        ]

        regex = (
            "<script({opt})*\\s+src=['\"]https://cdn"  # noqa: WPS342
            + "\\.ampproject\\.org/(lts/)?v0\\.m?js['\"]"  # noqa: WPS342
            + r"({opt})*\s*>\s*</script>"
        ).format(
            opt="|".join(r"\s+{}".format(pattern) for pattern in attribute_patterns),
        )

        if not re.search(regex, response_content):
            return response

        boilerplate_header = "Ignored"

        parser = AMPRenderer(
            runtime_version=settings.AMP_RUNTIME_VERSION,
            runtime_styles=settings.AMP_RUNTIME_STYLES,
        )

        parser.should_strip_comments = self.should_strip_comments
        parser.should_trim_attrs = self.should_trim_attrs
        response_content = parser.render(response_content)

        response.content = response_content
        response["Content-Length"] = len(response.content)

        if parser.no_boilerplate:
            boilerplate_header = "Removed"

        # Set a header on the response for downstream code to know
        # whether the boilerplate was removed.
        response["Boilerplate-Status"] = boilerplate_header

        return response
