# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

# Standard Library
from builtins import bytes  # noqa
from builtins import str  # noqa

# Third Party
from mock import MagicMock, Mock, patch

# AMP Renderer
from django_amp_renderer.middleware import AMPRenderingMiddleware

settings = Mock()
settings.AMP_RUNTIME_VERSION = '0123456789'
settings.AMP_RUNTIME_STYLES = 'body{background:pink;}'


@patch('django_amp_renderer.middleware.settings', new=settings)
class TestMiddleware:
    BOILERPLATE_HEADER_KEY = 'Boilerplate-Status'

    NON_TRIGGERING = '<!doctype html><html><head></head><body></body></html>'.encode('utf-8')
    TRIGGERING = [html.encode('utf-8') for html in [
        """
            <!doctype html>
            <html>
                <head>
                    <script async src="https://cdn.ampproject.org/v0.js" ></script>
                </head>
                <body>
                </body>
            </html>
        """,

        """
            <!doctype html>
            <html>
                <head>
                    <script async src="https://cdn.ampproject.org/v0.js" ></script>
                </head>
                <body>
                </body>
            </html>
        """,

        """
            <!doctype html>
            <html>
                <head>
                    <script async src="https://cdn.ampproject.org/v0.js" ></script>
                </head>
                <body>
                </body>
            </html>
        """,

        """
            <!doctype html>
            <html>
                <head>
                    <script type='module' async src="https://cdn.ampproject.org/lts/v0.js"></script>
                </head>
                <body>
                </body>
            </html>
        """,
    ]]

    def _get_response():
        return None

    def setup_method(self, method):
        request = Mock()
        request.META = MagicMock()
        request.GET = {}
        self.request = request

        response = MagicMock()
        response.has_header = MagicMock(return_value=True)
        headers = {'Content-Type': 'text/html'}
        response.__getitem__.side_effect = headers.__getitem__
        self.response = response

        self.middleware = AMPRenderingMiddleware(self._get_response)

    def teardown_method(self, method):
        del self.request
        del self.response
        del self.middleware

    @patch('django_amp_renderer.middleware.AMPRenderer')
    def test_non_triggering(self, MockAMPRenderer):  # noqa
        self.response.content = self.NON_TRIGGERING

        self.middleware.process_response(self.request, self.response)
        assert not MockAMPRenderer.called
        self.response.__setitem__.assert_not_called()

    def _setup_renderer(self, MockAMPRenderer):  # noqa
        self.renderer = MagicMock()
        self.renderer.render = MagicMock(return_value='Yay! HTML!')
        MockAMPRenderer.return_value = self.renderer

    @patch('django_amp_renderer.middleware.AMPRenderer')
    def test_triggering_1(self, MockAMPRenderer):  # noqa
        self._setup_renderer(MockAMPRenderer)

        self.response.content = self.TRIGGERING[0]

        self.middleware.process_response(self.request, self.response)

        assert MockAMPRenderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(self.BOILERPLATE_HEADER_KEY, 'Removed')

    @patch('django_amp_renderer.middleware.AMPRenderer')
    def test_triggering_2(self, MockAMPRenderer):  # noqa
        self._setup_renderer(MockAMPRenderer)

        self.response.content = self.TRIGGERING[1]

        self.middleware.process_response(self.request, self.response)

        assert MockAMPRenderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(self.BOILERPLATE_HEADER_KEY, 'Removed')

    @patch('django_amp_renderer.middleware.AMPRenderer')
    def test_triggering_3(self, MockAMPRenderer):  # noqa
        self._setup_renderer(MockAMPRenderer)

        self.response.content = self.TRIGGERING[2]

        self.middleware.process_response(self.request, self.response)

        assert MockAMPRenderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(self.BOILERPLATE_HEADER_KEY, 'Removed')

    @patch('django_amp_renderer.middleware.AMPRenderer')
    def test_triggering_4(self, MockAMPRenderer):  # noqa
        self._setup_renderer(MockAMPRenderer)

        self.response.content = self.TRIGGERING[3]

        self.middleware.process_response(self.request, self.response)

        assert MockAMPRenderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(self.BOILERPLATE_HEADER_KEY, 'Removed')

    @patch('django_amp_renderer.middleware.AMPRenderer')
    def test_not_html(self, MockAMPRenderer):  # noqa
        self.response.content = self.TRIGGERING[0]

        headers = {'Content-Type': 'application/json'}
        self.response.__getitem__.side_effect = headers.__getitem__

        self.middleware.process_response(self.request, self.response)

        assert not MockAMPRenderer.called
        self.response.__setitem__.assert_not_called()

    @patch('django_amp_renderer.middleware.AMPRenderer')
    def test_non_unicode(self, MockAMPRenderer):  # noqa
        self.response.content = 'õ'.encode('cp857')

        self.middleware.process_response(self.request, self.response)

        assert not MockAMPRenderer.called
        self.response.__setitem__.assert_not_called()
