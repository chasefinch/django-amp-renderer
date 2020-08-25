# Django AMP Renderer

![Python 2.7 & 3.5+](https://img.shields.io/badge/python-2.7%20%7C%203.5%2B-blue) ![Django 1.11+](https://img.shields.io/badge/django-%201.11%2B-blue) [![Build Status](https://travis-ci.com/chasefinch/django-amp-renderer.svg?branch=master)](https://travis-ci.com/chasefinch/django-amp-renderer) ![Coverage](https://img.shields.io/badge/coverage-0%25-red)

Middleware for applying [AMP Renderer](https://github.com/chasefinch/amp-renderer) to the output of a request in Django.

## Usage

Install via PyPI:
	
	pip install django-amp-renderer

To apply the middleware, add `django_amp_renderer.middleware.AMPRenderingMiddleware` to `MIDDLEWARE` in your Django settings file:

	MIDDLEWARE = [
	    'django_amp_renderer.middleware.AMPRenderingMiddleware',
	    …
	]

The middleware expects the variables `AMP_RUNTIME_VERSION` and `AMP_RUNTIME_STYLES` to be set in your Django settings file. For AMP_RUNTIME_VERSION, provide the current AMP runtime version number as a string (to avoid losing leading zeroes), and for AMP_RUNTIME_STYLES, provide the full contents of https://cdn.ampproject.org/v0.css.

	AMP_RUNTIME_VERSION = '012007242032002'
	AMP_RUNTIME_STYLES = """html{overflow-x:hidden!important}…"""

AMPRenderer has optional comment removal and attribute trimming. Those are disabled by default; To access them, use a subclass of the middleware and set the variables to `True`. They are passed along to the renderer.

	class TransformingMiddleware(AMPRenderingMiddleware):
	    should_strip_comments = True
	    should_trim_attributes = True

## Testing, etc.

Sort imports (Requires Python >= 3.6):

	make normal

Lint (Requires Python >= 3.6):

	make lint

Test:

	make test