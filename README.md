# Django Styleguide

Django styleguide used in [HackSoft](https://hacksoft.io) projects.

Expect often updates as we discuss & decide upon different things.

**Table of contents:**

<!-- toc -->

- [Overview](#overview)
- [Models](#models)
  * [Custom validation](#custom-validation)
  * [Properties](#properties)
  * [Methods](#methods)
  * [Testing](#testing)
- [Services](#services)
- [Selectors](#selectors)
- [APIs & Serializers](#apis--serializers)
  * [An example list API](#an-example-list-api)
  * [An example detail API](#an-example-detail-api)
  * [An example create API](#an-example-create-api)
  * [An example update API](#an-example-update-api)
  * [Nested serializers](#nested-serializers)
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

## Models

Lets take a look at an example model:

```python
class Course(models.Model):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    attendable = models.BooleanField(default=True)

    students = models.ManyToManyField(
        Student,
        through='CourseAssignment',
        through_fields=('course', 'student')
    )

    teachers = models.ManyToManyField(
        Teacher,
        through='CourseAssignment',
        through_fields=('course', 'teacher')
    )

    slug_url = models.SlugField(unique=True)

    repository = models.URLField(blank=True)
    video_channel = models.URLField(blank=True, null=True)
    facebook_group = models.URLField(blank=True, null=True)

    logo = models.ImageField(blank=True, null=True)

    public = models.BooleanField(default=True)

    generate_certificates_delta = models.DurationField(default=timedelta(days=15))

    objects = CourseManager()

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date cannot be before start date!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def visible_teachers(self):
        return self.teachers.filter(course_assignments__hidden=False).select_related('profile')

    @property
    def duration_in_weeks(self):
        weeks = rrule.rrule(
            rrule.WEEKLY,
            dtstart=self.start_date,
            until=self.end_date
        )
        return weeks.count()

    @property
    def has_started(self):
        now = get_now()

        return self.start_date <= now.date()

    @property
    def has_finished(self):
        now = get_now()

        return self.end_date <= now.date()

    @property
    def can_generate_certificates(self):
        now = get_now()

        return now.date() <= self.end_date + self.generate_certificates_delta

    def __str__(self) -> str:
        return self.name
```

Few things to spot here.

**Custom validation:**

* There's a custom model validation, defined in `clean`. This validation uses only model fields and no relations.
* This requires someone to call `full_clean()` on the model instance. The best place to do that is in the `save()` method of the model. Otherwise people can forget to call `full_clean()` in the respective service.

**Properties:**

* All properties, expect `visible_teachers` work directly on model fields.
* `visible_teachers` is a great candidate for a **selector**.

We have few general rules for custom validations & model properties / methods:

### Custom validation

* If the custom validation depends only on the **non-relational model fields**, define it in `clean` and call `full_clean` in `save`.
* If the custom validation is more complex & **spans relationships**, do it in the service that creates the model.
* It's OK to combine both `clean` and additional validation in the `service`.


### Properties

* If your model properties use only **non-relational model fields**, they are OK to stay as properties.
* If a property, such as `visible_teachers` starts **spanning relationships**, it's better to define a selector for that.


### Methods

* If you need a method that updates several fields at once (for example - `created_at` and `created_by` when something happens), you can create a model method that does the job.
* Every model method should be wrapped in a service. There should be no model method calling outside a service.

### Testing

Models need to be tested only if there's something additional to them - like custom validation or properties.

If we are strict & don't do custom validation / properties, then we can test the models without actually writing anything to the database => we are going to get quicker tests.

Foe example, if we want to test the custom validation, here's how a test could look like:

```python
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError

from odin.common.utils import get_now

from odin.education.factories import CourseFactory
from odin.education.models import Course


class CourseTests(TestCase):
    def test_course_end_date_cannot_be_before_start_date(self):
        start_date = get_now()
        end_date = get_now() - timedelta(days=1)

        course_data = CourseFactory.build()
        course_data['start_date'] = start_date
        course_data['end_date'] = end_date

        course = Course(**course_data)

        with self.assertRaises(ValidationError):
            course.full_clean()

```

There's a lot going on in this test:

* `get_now()` returns a timezone aware datetime.
* `CourseFactory.build()` will return a dictionary with all required fields for a course to exist.
* We replace the values for `start_date` and `end_date`.
* We assert that a validation error is going to be raised if we call `full_clean`.
* We are not hitting the database at all, since there's no need for that.

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


## Inspiration

The way we do Django is inspired by the following things:

* The general idea for **separation of concerns**
* [Boundaries by Gary Bernhardt](https://www.youtube.com/watch?v=yTkzNHF6rMs)
* Rails service objects
