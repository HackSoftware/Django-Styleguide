# Django Styleguide

Django styleguide used in [HackSoft](https://hacksoft.io) projects.

Expect often updates as we discuss & decide upon different things.

**Table of contents:**

<!-- toc -->

- [Overview](#overview)
- [Services](#services)
- [Selectors](#selectors)
- [APIs & Serializers](#apis--serializers)
  * [An example list API](#an-example-list-api)
  * [An example detail API](#an-example-detail-api)
  * [An example create API](#an-example-create-api)
  * [An example update API](#an-example-update-api)
  * [Nested serializers](#nested-serializers)
- [Exception Handling](#exception-handling)
  * [Raising Exceptions in Services](#raising-exceptions-in-services)
  * [Handle Exceptions in APIs](#handle-exceptions-in-apis)
- [Inspiration](#inspiration)

<!-- tocstop -->

## Overview

**In Django, business logic should live in:**

* Model properties (with some exceptions).
* Model `clean` method for additional validations (with some exceptions).
* Services - functions, that take care of code written to the database.
* Selectors - functions, that take care of code taken from the database.

**In Django, business logic should not live in:**

* APIs and Views.
* Serializers and Forms.
* Form tags.
* Model `save` method.

**Model properties vs selectors:**

* If the model property spans multiple relations, it should better be a selector.
* If a model property, added to some list API, will cause `N + 1` problem that cannot be easily solved with `select_related`, it should better be a selector.

## Services

A service is a simple function that:

* Lives in `your_app/services.py` module
* Takes keyword-only arguments
* Is type-annotated (even if you are not using `mypy` at the moment)
* Works mostly with models & other services and selectors
* Does business logic - from simple model creation to complex cross-cutting concerns, to calling external services & tasks.

An example service that creates an user:

```python
def create_user(
    *,
    email: str,
    name: str
) -> User:
    user = User(email=email)
    user.full_clean()
    user.save()

    create_profile(user=user, name=name)
    send_confirmation_email(user=user)

    return user
```

As you can see, this service calls 2 other services - `create_profile` and `send_confirmation_email`


## Selectors

A selector is a simple function that:

* Lives in `your_app/selectors.py` module
* Takes keyword-only arguments
* Is type-annotated (even if you are not using `mypy` at the moment)
* Works mostly with models & other services and selectors
* Does business logic around fetching data from your database

An example selector that list users from the database:

```python
def get_users(*, fetched_by: User) -> Iterable[User]:
    user_ids = get_visible_users_for(user=fetched_by)

    query = Q(id__in=user_ids)

    return User.objects.filter(query)
```

As you can see, `get_visible_users_for` is another selector.

## APIs & Serializers

When using services & selectors, all of your APIs should look simple & the same.

General rules for an API is:

* Do 1 API per operation. For CRUD on a model, this means 4 APIs.
* Use the most simple `APIView` or `GenericAPIView`
* Use services / selectors & don't do business logic in your API.
* Use serializers for fetching objects from params - passed either via `GET` or `POST`
* Serializer should be nested in the API and be named either `InputSerializer` or `OutputSerializer`
  * `OutputSerializer` can subclass `ModelSerializer`, if needed.
  * `InputSerializer` should always be a plain `Serializer`
  * Reuse serializers as little as possible
  * If you need a nested serializer, use the `inline_serializer` util

### An example list API

```python
class CourseListApi(SomeAuthenticationMixin, APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = ('id', 'name', 'start_date', 'end_date')

    def get(self, request):
        courses = get_courses()

        data = self.OutputSerializer(courses, many=True)

        return Response(data)
```

### An example detail API

```python
class CourseDetailApi(SomeAuthenticationMixin, APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = ('id', 'name', 'start_date', 'end_date')

    def get(self, request, course_id):
        course = get_course(id=course_id)

        data = self.OutputSerializer(course)

        return Response(data)
```

### An example create API

```python
class CourseCreateApi(SomeAuthenticationMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_course(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
```

### An example update API

```python
class CourseUpdateApi(SomeAuthenticationMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        start_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)

    def post(self, request, course_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        update_course(course_id=course_id, **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
```

### Nested serializers

In case you need to use a nested serializer, you can do the following thing:

```python
class Serializer(serializers.Serializer):
    weeks = inline_serializer(many=True, fields={
        'id': serializers.IntegerField(),
        'number': serializers.IntegerField(),
    })
```

The implementation of `inline_serializer` can be found in `utils.py` in this repo.


## Exception Handling

### Raising Exceptions in Services / Selectors

Now we have separation between our HTTP interface & the core logic of our application.

In order to keep this separation of concerns, our services and selectors must not use the `rest_framework.exception` classes because they are bounded with HTTP status codes. 

Our services and selectors must use one of:

* [Python built-in exceptions](https://docs.python.org/3/library/exceptions.html)
* Exceptions from `django.core.exceptions`
* Custom exceptions, inheriting from the ones above.

Here is a good example of service that preforms some validation and raises `django.core.exceptions.ValidationError`:

```python
from django.core.exceptions import ValidationError

def create_topic(*, name: str, course: Course) -> Topic:
    if course.end_date < timezone.now():
       raise ValidationError('You can not create topics for course that has ended.')

    topic = Topic.objects.create(name=name, course=course)

    return topic
```

### Handle Exceptions in APIs

In order to transform the exceptions raised in the services or selectors, to a standard HTTP response, you need to catch the exception and raise something that the rest framework understands.

The best place to do this is in the `handle_exception` method of the `APIView`.

There you can map your exception to DRF exception.

Here is an example:

```python
from rest_framework import exceptions as rest_exceptions

from django.core.exceptions import ValidationError


class CourseCreateApi(SomeAuthenticationMixin, APIView):
    expected_exceptions = {
        ValidationError: rest_exceptions.ValidationError
    }

    class InputSerializer(serializers.Serializer):
        ...

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_course(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
```

Here's the implementation of `get_error_message`:

```python
def get_first_matching_attr(obj, *attrs, default=None):
    for attr in attrs:
        if hasattr(obj, attr):
            return getattr(obj, attr)

    return default


def get_error_message(exc):
    if hasattr(exc, 'message_dict'):
        return exc.message_dict
    error_msg = get_first_matching_attr(exc, 'message', 'messages')

    if isinstance(error_msg, list):
        error_msg = ', '.join(error_msg)

    if error_msg is None:
        error_msg = str(exc)

    return error_msg
```

You can move this code to a mixin and use it in every API to prevent code duplication. 

We call this `ExceptionHandlerMixin`. Here's a sample implementation from one of our projects:

```python
from rest_framework import exceptions as rest_exceptions

from django.core.exceptions import ValidationError

from project.common.utils import get_error_message


class ExceptionHandlerMixin:
    """
    Mixin that transforms Django and Python exceptions into rest_framework ones.
    without the mixin, they return 500 status code which is not desired.
    """
    expected_exceptions = {
        ValueError: rest_exceptions.ValidationError,
        ValidationError: rest_exceptions.ValidationError,
        PermissionError: rest_exceptions.PermissionDenied
    }

    def handle_exception(self, exc):
        if isinstance(exc, tuple(self.expected_exceptions.keys())):
            drf_exception_class = self.expected_exceptions[exc.__class__]
            drf_exception = drf_exception_class(get_error_message(exc))

            return super().handle_exception(drf_exception)

        return super().handle_exception(exc)
```

Having this mixin in mind, our API can be written like that:

```python

class CourseCreateApi(
  SomeAuthenticationMixin,
  ExceptionHandlerMixin,
  APIView
):
    class InputSerializer(serializers.Serializer):
        ...

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_course(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
```

All of code above can be found in `utils.py` in this repository.

## Inspiration

The way we do Django is inspired by the following things:

* The general idea for **separation of concerns**
* [Boundaries by Gary Bernhardt](https://www.youtube.com/watch?v=yTkzNHF6rMs)
* Rails service objects
