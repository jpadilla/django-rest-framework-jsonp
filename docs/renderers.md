# Renderers

## Setting the renderers

The default set of renderers may be set globally, using the `DEFAULT_RENDERER_CLASSES` setting.  For example, the following settings would use `JSONP` as the main media type and also include the self describing API.

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework_jsonp.renderers.JSONPRenderer',
        )
    }

You can also set the renderers used for an individual view, or viewset,
using the `APIView` class based views.

    from django.contrib.auth.models import User
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from rest_framework_jsonp.renderers import JSONPRenderer

    class UserCountView(APIView):
        """
        A view that returns the count of active users in JSONP.
        """
        renderer_classes = (JSONPRenderer,)

        def get(self, request, format=None):
            user_count = User.objects.filter(active=True).count()
            content = {'user_count': user_count}
            return Response(content)

Or, if you're using the `@api_view` decorator with function based views.

    @api_view(['GET'])
    @renderer_classes((JSONPRenderer,))
    def user_count_view(request, format=None):
        """
        A view that returns the count of active users in JSONP.
        """
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)

---

# API Reference

## JSONPRenderer

Renders the request data into `JSONP`.  The `JSONP` media type provides a mechanism of allowing cross-domain AJAX requests, by wrapping a `JSON` response in a javascript callback.

The javascript callback function must be set by the client including a `callback` URL query parameter.  For example `http://example.com/api/users?callback=jsonpCallback`.  If the callback function is not explicitly set by the client it will default to `'callback'`.

---

**Warning**: If you require cross-domain AJAX requests, you should almost certainly be using the more modern approach of [CORS][cors] as an alternative to `JSONP`.  See the [CORS documentation][cors-docs] for more details.

The `jsonp` approach is essentially a browser hack, and is [only appropriate for globally  readable API endpoints][jsonp-security], where `GET` requests are unauthenticated and do not require any user permissions.

---

**.media_type**: `application/javascript`

**.format**: `'.jsonp'`

**.charset**: `utf-8`


[cors]: http://www.w3.org/TR/cors/
[cors-docs]: http://www.django-rest-framework.org/topics/ajax-csrf-cors/
[jsonp-security]: http://stackoverflow.com/questions/613962/is-jsonp-safe-to-use
