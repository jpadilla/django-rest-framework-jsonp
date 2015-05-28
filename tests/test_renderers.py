# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.settings import api_settings

from rest_framework_jsonp.renderers import JSONPRenderer


class MockGETView(APIView):
    def get(self, request, **kwargs):
        return Response({'foo': ['bar', 'baz']})


urlpatterns = patterns(
    '',
    url(r'^jsonp/jsonrenderer$', MockGETView.as_view(renderer_classes=[JSONRenderer, JSONPRenderer])),
    url(r'^jsonp/nojsonrenderer$', MockGETView.as_view(renderer_classes=[JSONPRenderer])),
)

# DRF 3.0 introduced COMPACT_JSON=True
if getattr(api_settings, 'COMPACT_JSON', None):
    _flat_repr = '{"foo":["bar","baz"]}'
else:
    _flat_repr = '{"foo": ["bar", "baz"]}'


class JSONPRendererTests(TestCase):
    """
    Tests specific to the JSONP Renderer
    """

    urls = 'tests.test_renderers'

    def test_without_callback_with_json_renderer(self):
        """
        Test JSONP rendering with View JSON Renderer.
        """
        resp = self.client.get(
            '/jsonp/jsonrenderer',
            HTTP_ACCEPT='application/javascript'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Content-Type'], 'application/javascript; charset=utf-8')
        self.assertEqual(
            resp.content,
            ('callback(%s);' % _flat_repr).encode('ascii')
        )

    def test_without_callback_without_json_renderer(self):
        """
        Test JSONP rendering without View JSON Renderer.
        """
        resp = self.client.get(
            '/jsonp/nojsonrenderer',
            HTTP_ACCEPT='application/javascript'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Content-Type'], 'application/javascript; charset=utf-8')
        self.assertEqual(
            resp.content,
            ('callback(%s);' % _flat_repr).encode('ascii')
        )

    def test_with_callback(self):
        """
        Test JSONP rendering with callback function name.
        """
        callback_func = 'myjsonpcallback'
        resp = self.client.get(
            '/jsonp/nojsonrenderer?callback=' + callback_func,
            HTTP_ACCEPT='application/javascript'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Content-Type'], 'application/javascript; charset=utf-8')
        self.assertEqual(
            resp.content,
            ('%s(%s);' % (callback_func, _flat_repr)).encode('ascii')
        )

    def test_with_invalid_callback(self):
        """
        Test JSONP rendering with a potentially dangerous callback function
        name.
        """
        callback_func = 'my.jsonp.callback'
        resp = self.client.get(
            '/jsonp/nojsonrenderer?callback=' + callback_func,
            HTTP_ACCEPT='application/javascript'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp['Content-Type'], 'application/javascript; charset=utf-8')
        self.assertEqual(
            resp.content,
            ('callback(%s);' % _flat_repr).encode('ascii')
        )
