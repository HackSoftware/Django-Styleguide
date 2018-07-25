# Django Styleguide

Django styleguide used in [HackSoft](https://hacksoft.io) projects.

Expect often updates as we discuss & decide upon different things.

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
