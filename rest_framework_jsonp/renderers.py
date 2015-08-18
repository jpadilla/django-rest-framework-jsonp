"""
Provides JSONP rendering support.
"""
from __future__ import unicode_literals

from rest_framework.renderers import JSONRenderer


class JSONPRenderer(JSONRenderer):
    """
    Renderer which serializes to json,
    wrapping the json output in a callback function.
    """

    media_type = 'application/javascript'
    format = 'jsonp'
    callback_parameter = 'callback'
    default_callback = 'callback'
    charset = 'utf-8'

    def get_callback(self, renderer_context):
        """
        Determine the name of the callback to wrap around the json output.
        """
        request = renderer_context.get('request', None)
        params = (request and getattr(request, 'query_params', False) or
                  getattr(request, 'QUERY_PARAMS', {}))
        return params.get(self.callback_parameter, self.default_callback)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders into jsonp, wrapping the json output in a callback function.

        Clients may set the callback function name using a query parameter
        on the URL, for example: ?callback=exampleCallbackName
        """
        renderer_context = renderer_context or {}
        callback = self.get_callback(renderer_context)
        json = super(JSONPRenderer, self).render(data, accepted_media_type,
                                                 renderer_context)
        return callback.encode(self.charset) + b'(' + json + b');'
