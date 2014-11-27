<div class="badges">
    <a href="http://travis-ci.org/jpadilla/django-rest-framework-jsonp?branch=master">
        <img src="https://travis-ci.org/jpadilla/django-rest-framework-jsonp.svg?branch=masterr">
    </a>
    <a href="https://pypi.python.org/pypi/djangorestframework-jsonp">
        <img src="https://pypip.in/version/djangorestframework-jsonp/badge.svg">
    </a>
</div>

---

# REST Framework JSONP

JSONP support for Django REST Framework

---

## Overview

JSONP support extracted as a third party package directly from the official Django REST Framework implementation.

## Requirements

* Python (2.7, 3.3, 3.4)
* Django (1.6, 1.7)

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

## Testing

Install testing requirements.

```bash
$ pip install -r requirements-test.txt
```

Run with runtests.

```bash
$ ./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
$ pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
$ mkdocs build
```
