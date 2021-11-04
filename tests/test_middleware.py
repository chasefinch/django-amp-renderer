"""Test the Django AMP Renderer package."""

# Third Party
from mock import MagicMock, Mock, patch

# Django AMP Renderer
# AMP Renderer
from django_amp_renderer.middleware import AMPRenderingMiddleware

settings = Mock()
settings.AMP_RUNTIME_VERSION = "X0123456789"
settings.AMP_RUNTIME_STYLES = "body{background:pink;}"


BOILERPLATE_HEADER_KEY = "Boilerplate-Status"
NON_TRIGGERING = "<!doctype html><html><head></head><body></body></html>".encode("utf-8")
triggering_1 = """
    <!doctype html>
    <html>
        <head>
            <script async src="https://cdn.ampproject.org/v0.js" ></script>
        </head>
        <body>
        </body>
    </html>
"""
triggering_2 = """
    <!doctype html>
    <html>
        <head>
            <script async src="https://cdn.ampproject.org/v0.js" ></script>
        </head>
        <body>
        </body>
    </html>
"""
triggering_3 = """
    <!doctype html>
    <html>
        <head>
            <script async src="https://cdn.ampproject.org/v0.js" ></script>
        </head>
        <body>
        </body>
    </html>
"""
triggering_4 = """
    <!doctype html>
    <html>
        <head>
            <script
                type='module'
                crossorigin="anonymous"
                async src="https://cdn.ampproject.org/lts/v0.js"
            ></script>
        </head>
        <body>
        </body>
    </html>
"""

TRIGGERING = tuple(
    [html.encode("utf-8") for html in (triggering_1, triggering_2, triggering_3, triggering_4)],
)


@patch("django_amp_renderer.middleware.settings", new=settings)
class TestMiddleware:
    """Test the Django AMP Rendering middleware."""

    def setup_method(self, method):
        """Set up a middleware with mock request values."""
        request = Mock()
        request.META = MagicMock()
        request.GET = {}
        self.request = request

        response = MagicMock()
        response.has_header = MagicMock(return_value=True)
        headers = {"Content-Type": "text/html"}
        response.__getitem__.side_effect = headers.__getitem__
        self.response = response

        self.middleware = AMPRenderingMiddleware(self._get_response)

    def teardown_method(self, method):
        """Clean up."""
        del self.request
        del self.response
        del self.middleware

    @patch("django_amp_renderer.middleware.AMPRenderer")
    def test_non_triggering(self, mock_amp_renderer):
        """Test a response that doesn't trigger the renderer."""
        self.response.content = NON_TRIGGERING

        self.middleware.process_response(self.request, self.response)
        assert not mock_amp_renderer.called
        self.response.__setitem__.assert_not_called()

    @patch("django_amp_renderer.middleware.AMPRenderer")
    def test_triggering_1(self, mock_amp_renderer):
        """Test #1."""
        self._setup_renderer(mock_amp_renderer)

        self.response.content = TRIGGERING[0]

        self.middleware.process_response(self.request, self.response)

        assert mock_amp_renderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(BOILERPLATE_HEADER_KEY, "Removed")

    @patch("django_amp_renderer.middleware.AMPRenderer")
    def test_triggering_2(self, mock_amp_renderer):
        """Test #2."""
        self._setup_renderer(mock_amp_renderer)

        self.response.content = TRIGGERING[1]

        self.middleware.process_response(self.request, self.response)

        assert mock_amp_renderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(BOILERPLATE_HEADER_KEY, "Removed")

    @patch("django_amp_renderer.middleware.AMPRenderer")
    def test_triggering_3(self, mock_amp_renderer):
        """Test #3."""
        self._setup_renderer(mock_amp_renderer)

        self.response.content = TRIGGERING[2]

        self.middleware.process_response(self.request, self.response)

        assert mock_amp_renderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(BOILERPLATE_HEADER_KEY, "Removed")

    @patch("django_amp_renderer.middleware.AMPRenderer")
    def test_triggering_4(self, mock_amp_renderer):
        """Test #4."""
        self._setup_renderer(mock_amp_renderer)

        self.response.content = TRIGGERING[3]

        self.middleware.process_response(self.request, self.response)

        assert mock_amp_renderer.called
        self.renderer.render.assert_called_once()
        self.response.__setitem__.assert_called_with(BOILERPLATE_HEADER_KEY, "Removed")

    @patch("django_amp_renderer.middleware.AMPRenderer")
    def test_not_html(self, mock_amp_renderer):
        """Test a non-HTML response."""
        self.response.content = TRIGGERING[0]

        headers = {"Content-Type": "application/json"}
        self.response.__getitem__.side_effect = headers.__getitem__

        self.middleware.process_response(self.request, self.response)

        assert not mock_amp_renderer.called
        self.response.__setitem__.assert_not_called()

    @patch("django_amp_renderer.middleware.AMPRenderer")
    def test_non_unicode(self, mock_amp_renderer):
        """Test a non-unicode response."""
        self.response.content = "õ".encode("cp857")

        self.middleware.process_response(self.request, self.response)

        assert not mock_amp_renderer.called
        self.response.__setitem__.assert_not_called()

    def _setup_renderer(self, mock_amp_renderer):
        self.renderer = MagicMock()
        self.renderer.render = MagicMock(return_value="Yay! HTML!")
        mock_amp_renderer.return_value = self.renderer

    def _get_response(self):
        pass
