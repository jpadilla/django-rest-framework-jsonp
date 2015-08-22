# REST Framework JSONP

[![build-status-image]][travis]
[![pypi-version]][pypi]

**JSONP support for Django REST Framework**

Full documentation for the project is available at [http://jpadilla.github.io/django-rest-framework-jsonp][docs].

## Overview

JSONP support extracted as a third party package directly from the official Django REST Framework implementation.

---

**Warning**: If you require cross-domain AJAX requests, you should almost certainly be using the more modern approach of [CORS][cors] as an alternative to `JSONP`. See the [CORS documentation][cors-docs] for more details.

The `jsonp` approach is essentially a browser hack, and is [only appropriate for globally  readable API endpoints][jsonp-security], where `GET` requests are unauthenticated and do not require any user permissions.

---

## Requirements

* Python (2.7, 3.3, 3.4)
* Django (1.6, 1.7, 1.8)
* Django REST Framework (2.4, 3.0, 3.1, 3.2)

## Installation

Install using `pip`...

```bash
$ pip install djangorestframework-jsonp
```

## Example

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_jsonp.renderers.JSONPRenderer',
    ),
}
```

You can also set the renderer used for an individual view, or viewset, using the APIView class based views.

```python
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jsonp.renderers import JSONPRenderer

class ExampleView(APIView):
    """
    A view that returns the count of active users in JSONP
    """
    renderer_classes = (JSONPRenderer,)

    def post(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)
```

## Documentation & Support

Full documentation for the project is available at [http://jpadilla.github.io/django-rest-framework-jsonp][docs].

You may also want to follow the [author][jpadilla] on Twitter.


[build-status-image]: https://secure.travis-ci.org/jpadilla/django-rest-framework-jsonp.svg?branch=master
[travis]: http://travis-ci.org/jpadilla/django-rest-framework-jsonp?branch=master
[pypi-version]: https://img.shields.io/pypi/v/djangorestframework-jsonp.svg
[pypi]: https://pypi.python.org/pypi/djangorestframework-jsonp
[cors]: http://www.w3.org/TR/cors/
[cors-docs]: http://www.django-rest-framework.org/topics/ajax-csrf-cors/
[jsonp-security]: http://stackoverflow.com/questions/613962/is-jsonp-safe-to-use
[docs]: http://jpadilla.github.io/django-rest-framework-jsonp
[jpadilla]: https://twitter.com/jpadilla_
