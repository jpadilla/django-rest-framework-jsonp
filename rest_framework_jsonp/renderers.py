"""
Provides JSONP rendering support.
"""
from __future__ import unicode_literals

import re

from rest_framework.renderers import JSONRenderer


class JSONPRenderer(JSONRenderer):
    """
    Renderer which serializes to json,
    wrapping the json output in a callback function.
    """

    media_type = 'application/javascript'
    format = 'jsonp'
    callback_parameter = 'callback'
    # alpha numeric characters and underscore only up to 100 characters length.
    callback_re = re.compile('^[a-zA-Z0-9_]{1,100}$')
    default_callback = 'callback'
    charset = 'utf-8'

    def get_callback(self, renderer_context):
        """
        Determine the name of the callback to wrap around the json output.
        """
        request = renderer_context.get('request', None)
        params = request and request.QUERY_PARAMS or {}
        cb_name = params.get(self.callback_parameter)

        if not (cb_name and self.callback_re.match(cb_name)):
            # If there is no custom callback or custom one does not match
            # callback_re default to default_callback.
            cb_name = self.default_callback

        return cb_name

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
