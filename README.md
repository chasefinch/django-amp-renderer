# Django AMP Renderer

![Python 3.10 | 3.11 | 3.12 | 3.13 | 3.14](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue) [![Build](https://github.com/chasefinch/django-amp-renderer/actions/workflows/build.yml/badge.svg)](https://github.com/chasefinch/django-amp-renderer/actions/workflows/build.yml) ![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

Middleware for applying [AMP Renderer](https://github.com/chasefinch/amp-renderer) to the output of a request in Django. Tested in Python 3.8 and above, but works on Python 3.6+.

## Usage

Install via PyPI:

	pip install django-amp-renderer

To apply the middleware, add `django_amp_renderer.AMPRenderingMiddleware` to `MIDDLEWARE` in your Django settings file:

	MIDDLEWARE = [
	    'django_amp_renderer.AMPRenderingMiddleware',
	    …
	]

The middleware expects the variables `AMP_RUNTIME_VERSION` and `AMP_RUNTIME_STYLES` to be set in your Django settings file.

For `AMP_RUNTIME_VERSION`, provide the current AMP runtime version number as a string (to avoid losing leading zeroes). For `AMP_RUNTIME_STYLES`, provide the full contents of https://cdn.ampproject.org/v0.css.

	AMP_RUNTIME_VERSION = '012007242032002'
	AMP_RUNTIME_STYLES = """
	    html{overflow-x:hidden!important}…
	""".strip()

AMPRenderer has optional comment removal and attribute trimming. Those are disabled by default; To access them, use a subclass of the middleware and set the variables to `True`. They are passed along to the renderer.

	class TransformingMiddleware(AMPRenderingMiddleware):
	    strip_comments = True
	    trim_attributes = True

You can apply the middleware to all requests, even non-AMP pages. The transformations will only be applied if the document contains the v0.js script (`https://cdn.ampproject.org/v0.js`).

If the transformation is applied, the `Boilerplate-Status` header of the response will either be set to "Removed" or "Ignored", based on whether the boilerplate was able to be removed by the renderer.

## Testing, etc.

Install development requirements (Requires Python >= 3.8):

	make install

Sort imports:

	make format

Lint:

	make lint

Test:

	make test
