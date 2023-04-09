# Django 风格指南

> 👀 你的 Django 项目需要帮助？[HackSoft](https://www.hacksoft.io/) 可以为你简化操作。请通过[consulting@hacksoft.io](mailto:consulting@hacksoft.io)联系我们

![Django Styleguide](https://github.com/EliaoHame/Django-Styleguide/raw/master/logo.png)

**Table of contents:**

[toc]



## 如何提出问题或建议？

以下是一些指导点，帮助您进行导航：

1. 如果你已经阅读了 Django 风格指南，并且有问题或建议，**最简单的方法就是打开一个问题（issue）**。我们会进行回复
2. 即使你有一个问题，不确定它是否与 Django 风格指南有关，**也可以打开一个问题（issue）**。我们会进行回复
3. 如果您想查看代码示例，请务必前往[Django Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example)代码库。我们将其视为“Django 测试项目”，结合最佳实践和来自[examples from our blog](https://www.hacksoft.io/blog)的示例

好的，就是这样 ✨

## 这是什么？

你好  👋

这是 Django 风格指南，由 [HackSoft](https://hacksoft.io/) 团队创建

**以下是关于 Django 风格指南的几个重要说明：**

1. 这个指南基于多年的经验和许多不同规模的 Django 项目
2. 它是实用的，这里提到的所有内容都经过了在生产环境中的测试
3. 它是有见解的，这是我们如何使用 Django 构建应用程序。
4. 但这并不是唯一的方法。有其他的方式来构建和组织 Django 项目，可以为你完成工作
5. 我们还有一个 [`Django-Styleguide-Example`](https://github.com/HackSoftware/Styleguide-Example)示例项目，可以展示大部分风格指南在实际项目中的应用

**您可以观看[Django structure for scale and longevity](https://www.youtube.com/watch?v=yG3ZdxBb1oo) 结构指南，了解风格指南背后的哲学：**

![Django structure for scale and longevity by Radoslav Georgiev](https://camo.githubusercontent.com/2f24e915f4e7379e27bcc2f18ae58018b6e158d0a1014d1d7aa46545933a23e2/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f7947335a64784262316f6f2f302e6a7067)

您还可以观看 Radoslav Georgiev 和 Ivaylo Bachvarov  **[discussion on HackCast, around the Django Styleguide](https://www.youtube.com/watch?v=9VfRaPECbpY)**：

![HackCast S02E08 - Django Community & Django Styleguide](https://camo.githubusercontent.com/e6c04dd711d282a8a89e62d4922e98744f9d214f89dcacb5319d178b22df65af/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f39566652615045436270592f302e6a7067)

## 如何使用它

使用 Django 风格指南有**三种常见方式**：

1. 严格按照这里写的所有内容
2. 根据你的特定情况选择有意义的部分
3. 不遵循这里写的任何内容

**我们推荐使用第二种方式:**

* 阅读风格指南
* 决定什么最适合你
* 根据您的具体情况进行调整

## 概述

Django风格指南的核心总结如下

**在Django中业务逻辑应该存在于**

* Services-函数为主，主要负责将事务写入数据库
* Selectors-函数为主，主要负责从数据库中获取事务
* 模型属性
* 模型`clean`方法进行额外验证

**在Django中，业务逻辑不应该存在于**

* API和视图
* 序列化器和表单
* 表单 tags
* 模型保存方法中
* 自定义管理器或查询集
* 信号

**模型属性与 selectors**

* 如果该属性涵盖多个关系，则最好将其作为 selector
* 如果该属性不太常规，并且在序列化时容易引起N + 1查询问题，则最好将其作为 selector



> Q: Why not put your business logic in APIs / Views / Serializers / Forms?
>
> A: 依靠通用的API /视图，并结合序列化器和表单，会有两个主要问题：
>
> 将业务逻辑分散在多个地方，使数据流程难以追踪。 隐藏了某些内容。为了更改某些内容，您需要了解您正在使用的抽象层的内部工作原理。 通用API和视图，结合序列化器和表单，非常适用于直接的“CRUD模型”情况。
>
> 根据我们迄今为止的经验，这种直接的情况很少发生。一旦你离开了幸福的CRUD路径，事情就开始变得混乱起来。
>
> 一旦事情开始变得混乱，您需要更多的“框”，以更好地组织您的代码。
>
> 这个样式指南的目的是：
>
> 给你那些“框”。 帮助您找出自己的“框”，以满足您自己特定的上下文和需求。
>
> Q: Why not put your business logic in custom managers and/or querysets?
>
> A: 这实际上是一个好主意，您可以引入自定义管理器和查询集，以公开更适合您领域的API。
>
> 但是，尝试将所有业务逻辑放在自定义管理器中并不是一个好主意，因为有以下原因：
>
> 业务逻辑具有其自己的领域，不总是直接映射到您的数据模型（models） 业务逻辑通常跨越多个模型，因此很难选择要放置的位置。 假设您有一个自定义逻辑片段，涉及模型A，B，C和D。您把它放在哪里？ 可能还需要调用第三方系统。您不希望将这些调用放在自定义管理器方法中。 这个想法是让您的领域与数据模型和API层分开。
>
> 如果我们将具有自定义查询集/管理器的想法与让领域分开的想法相结合，我们将得到我们所谓的“服务层”。
>
> 服务可以是函数、类、模块或任何对您特定情况有意义的东西。
>
> 有了这些想法，自定义管理器和查询集是非常强大的工具，应用于为模型公开更好的接口。
>
> Q:  Why not put your business logic in signals?
>
> A: 在所有可用选项中，也许这个选项很快就会让您走向非常糟糕的地方：
>
> 信号是将不应该互相知道的事物连接在一起的好工具，但您希望它们保持连接。 信号也是在您的业务逻辑层之外处理缓存失效的好工具。 如果我们开始使用信号来连接密切相关的事物，我们只是让连接更加隐式，使其更难以跟踪数据流。 
>
> 这就是为什么我们建议仅在非常特定的情况下使用信号，但通常不建议将其用于构建域/业务层的原因。

### 项目模版示例

建议使用 Cookie Cutter 为每个新项目提供某种模板

* [`Styleguide-Example`](https://github.com/HackSoftware/Styleguide-Example)
* [`cookiecutter-django`](https://github.com/pydanny/cookiecutter-django)
* [cookiecutter](https://cookiecutter.readthedocs.io/en/latest/)

## 模型

模型应该只关注数据模型而不是其它

### 基础模型

不同模型使用相同的字段时，像  `created_at` 和 `updated_at` 。可以把它们放到 base model 当中然后在继承这个 **base model** 。定义的主键也可以放到 **base model** 中，例如：**UUIDField**

代码示例：

```python
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

当需要一个新模型时，只需继承BaseModel即可

### 校验方法 clean 和 full_clean

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")
```

在定义模型 `clean` 方法，因为要确保在将数据保存到数据库中时得到好的数据。为了调用clean方法，必须在保存之前对模型实例调用full_clean方法

**建议在调用保存之前，在服务中执行这个操作**

```python
def course_create(*, name: str, start_date: date, end_date: date) -> Course:
    obj = Course(name=name, start_date=start_date, end_date=end_date)

    obj.full_clean()
    obj.save()

    return obj
```

**关于何时在模型的clean方法中添加验证的一般准则**

1.  如果我们基于模型的多个非关联字段进行验证
2. 如果验证本身足够简单

**将验证移动到服务层的一般准则**

1. 验证逻辑更复杂
2. 需要跨关联和获取其他数据

> ​	如果情况需要，可以在clean和服务中都进行验证，但如果是这种情况，我们倾向于在服务层进行验证

### 校验方法-约束

可以使用Django的约束条件进行验证，应该以此为目标

写的代码越少，需要维护的代码也就越少，即使数据来自不同的位置，数据库也会处理数据

```python
class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="start_date_before_end_date",
                check=Q(start_date__lt=F("end_date"))
            )
        ]
```

如果我们尝试通过course.save()或Course.objects.create(...)创建新对象，我们将得到一个IntegrityError，而不是ValidationError。

这实际上可能是一个缺点（从Django 4.1开始不再是这样。请查看下面的额外部分），因为现在，我们必须处理IntegrityError，它并不总是有最好的错误消息

> 自Django 4.1开始，调用.full_clean也会检查模型约束条件！
>
> 这实际上消除了上述缺点，因为如果您的模型约束条件未通过检查，则会得到一个很好的ValidationError（如果您通过Model.objects.create(...)进行操作，则仍存在缺点）。
>
> 有关更多信息，请参见https://docs.djangoproject.com/en/4.1/ref/models/instances/#validating-objects
>
> 有关示例测试用例，请查看Styleguide-Example repo-https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/tests/models/test_random_model.py#L12

Django的约束条件文档非常简洁，因此可以查看Adam Johnson的以下文章，以了解如何使用它们

1. [Using Django Check Constraints to Ensure Only One Field Is Set](https://adamj.eu/tech/2020/03/25/django-check-constraints-one-field-set/)
2. [Django’s Field Choices Don’t Constrain Your Data](https://adamj.eu/tech/2020/01/22/djangos-field-choices-dont-constrain-your-data/)
3. [Using Django Check Constraints to Prevent Self-Following](https://adamj.eu/tech/2021/02/26/django-check-constraints-prevent-self-following/)

### 属性

模型属性是从模型实例快速访问派生值的好方法

例如，让我们来看一下我们Course模型的has_started和has_finished属性：

```python
from django.utils import timezone
from django.core.exceptions import ValidationError


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")

    @property
    def has_started(self) -> bool:
        now = timezone.now()

        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()

        return self.end_date <= now.date()
```

这些属性非常方便，因为我们现在可以在序列化器中引用它们或在模板中使用

**何时向模型添加属性，一般的准则**

1. 如果我们需要一个基于非关联模型字段的简单派生值，请添加一个@property
2. 如果计算派生值足够简单

**在以下情况下，属性应该是其他东西（service, selector, utility)**

1. 如果我们需要跨多个关联或获取其他数据
2. 如果计算更复杂

### 方法

模型方法也是非常强大的工具，可以在属性的基础上构建

例如下方代码中的 `is_within(self, x)` 方法：

```python
from django.core.exceptions import ValidationError
from django.utils import timezone


class Course(BaseModel):
    name = models.CharField(unique=True, max_length=255)

    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")

    @property
    def has_started(self) -> bool:
        now = timezone.now()

        return self.start_date <= now.date()

    @property
    def has_finished(self) -> bool:
        now = timezone.now()

        return self.end_date <= now.date()

    def is_within(self, x: date) -> bool:
        return self.start_date <= x <= self.end_date
```

`is_within` 不是一种属性，因为它要求参数。所以用方法代替。

在模型中使用方法的另一个绝佳方式是将其用于属性设置，当设置一个属性必须始终紧跟着设置另一个具有派生值的属性时。

例如：

```python
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone


class Token(BaseModel):
    secret = models.CharField(max_length=255, unique=True)
    expiry = models.DateTimeField(blank=True, null=True)

    def set_new_secret(self):
        now = timezone.now()

        self.secret = get_random_string(255)
        self.expiry = now + settings.TOKEN_EXPIRY_TIMEDELTA

        return self
```

这样就可以安全的调用 `set_new_secret` 设置正确的 `secret`和 `expiry`

**何时向模型添加方法**

1. 需要一个简单的派生值，需要基于非关系型模型字段的参数
2. 计算派生值的过程足够简单
3. 设置一个属性总是需要设置其他属性的值
4. 以下情况下，模型应该是其他东西（**service, selector, utility**）
   1. 需要跨多个关系或获取其他数据
   2. 计算更为复杂

### 测试

如果模型具有额外的内容，如验证、属性或方法等，那么才需要对模型进行测试。这意味着模型需要被测试以确保这些额外的内容的正确性和有效性。如果模型只是一个简单的数据结构，那么就不需要进行测试，因为这些结构本身就是很基础的，没有什么需要额外测试的内容

```python
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from project.some_app.models import Course


class CourseTests(TestCase):
    def test_course_end_date_cannot_be_before_start_date(self):
        start_date = timezone.now()
        end_date = timezone.now() - timedelta(days=1)

        course = Course(start_date=start_date, end_date=end_date)

        with self.assertRaises(ValidationError):
            course.full_clean()
```

这里需要注意几点

1. 如果我们断言调用 "full_clean" 方法，就会引发验证错误
2. 不需要访问数据库，因为没有必要。可以加快某些测试的速度

## 服务层

服务层是业务逻辑所在的地方，可以访问数据库和其他资源，并可以与系统的其他部分交互

![](https://user-images.githubusercontent.com/387867/134778130-be168592-b953-4b74-8588-a3dbaa0b6871.png)

服务可以是：

* 一个简单的函数
* 一个类
* 一个完整的模块
* 也可以是在特定情况下合适的任何东西

在大多数情况下，服务可以是一个简单的函数：

* 位于 `<your_app>/services.py` 模块中
* 接受关键字参数，除非它不需要参数或只需要一个参数
* 进行类型注释（即使当前未使用mypy）
* 与数据库、其他资源和系统的其他部分进行交互
* 执行业务逻辑 - 包括简单的模型创建、复杂的横跨多个模块的逻辑、调用外部服务和任务等

### 基于函数的服务示例

创建用户的示例服务：

```python
def user_create(
    *,
    email: str,
    name: str
) -> User:
    user = User(email=email)
    user.full_clean()
    user.save()

    profile_create(user=user, name=name)
    confirmation_email_send(user=user)

    return user
```

如你所见，这个服务调用了两个其他服务 `profile_create` 和 `confirmation_email_send`

在这个示例中，所有与用户创建相关的内容都集中在一个地方，并且可以被追踪到。这样的架构使得代码更易于维护和修改。如果需要更改用户创建逻辑，可以在一个地方修改它，而无需在整个代码库中查找并修改相关的代码。此外，这种架构也促进了代码重用，因为这些服务可以在应用程序中的其他地方重复使用，而无需重新编写或复制粘贴相同的代码

### 基于类的服务示例

此外，我们还可以使用“基于类”的服务，这是一种将逻辑封装在类中的高级方式

以下是一个直接从Django风格指南示例中提取的与文件上传相关的示例：

```python
# https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/services.py


class FileStandardUploadService:
    """
    This also serves as an example of a service class,
    which encapsulates 2 different behaviors (create & update) under a namespace.

    Meaning, we use the class here for:

    1. The namespace
    2. The ability to reuse `_infer_file_name_and_type` (which can also be an util)
    """
    def __init__(self, user: BaseUser, file_obj):
        self.user = user
        self.file_obj = file_obj

    def _infer_file_name_and_type(self, file_name: str = "", file_type: str = "") -> Tuple[str, str]:
        if not file_name:
            file_name = self.file_obj.name

        if not file_type:
            guessed_file_type, encoding = mimetypes.guess_type(file_name)

            if guessed_file_type is None:
                file_type = ""
            else:
                file_type = guessed_file_type

        return file_name, file_type

    @transaction.atomic
    def create(self, file_name: str = "", file_type: str = "") -> File:
        _validate_file_size(self.file_obj)

        file_name, file_type = self._infer_file_name_and_type(file_name, file_type)

        obj = File(
            file=self.file_obj,
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            uploaded_by=self.user,
            upload_finished_at=timezone.now()
        )

        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def update(self, file: File, file_name: str = "", file_type: str = "") -> File:
        _validate_file_size(self.file_obj)

        file_name, file_type = self._infer_file_name_and_type(file_name, file_type)

        file.file = self.file_obj
        file.original_file_name = file_name
        file.file_name = file_generate_name(file_name)
        file.file_type = file_type
        file.uploaded_by = self.user
        file.upload_finished_at = timezone.now()

        file.full_clean()
        file.save()

        return file
```

使用这种方法有两个主要原因：

1. **命名空间**。我们为创建和更新操作提供了一个单一的命名空间
2. **重用** `_infer_file_name_and_type` 方法

如何使用这个服务的示例：

```python
# https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/apis.py

class FileDirectUploadApi(ApiAuthMixin, APIView):
    def post(self, request):
        service = FileDirectUploadService(
            user=request.user,
            file_obj=request.FILES["file"]
        )
        file = service.create()

        return Response(data={"id": file.id}, status=status.HTTP_201_CREATED)
```

```python
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    # ... other code here ...
    # https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/admin.py

    def save_model(self, request, obj, form, change):
        try:
            cleaned_data = form.cleaned_data

            service = FileDirectUploadService(
                file_obj=cleaned_data["file"],
                user=cleaned_data["uploaded_by"]
            )

            if change:
                service.update(file=obj)
            else:
                service.create()
        except ValidationError as exc:
            self.message_user(request, str(exc), messages.ERROR)
```

对于涉及多个步骤的“流程”，使用基于类的服务是一个好主意

例如，以下服务代表了一个“直接文件上传流程”，其中有一个 `start` 和 `end`（以及其他的中间步骤)：

```python
# https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/services.py


class FileDirectUploadService:
    """
    This also serves as an example of a service class,
    which encapsulates a flow (start & finish) + one-off action (upload_local) into a namespace.

    Meaning, we use the class here for:

    1. The namespace
    """
    def __init__(self, user: BaseUser):
        self.user = user

    @transaction.atomic
    def start(self, *, file_name: str, file_type: str) -> Dict[str, Any]:
        file = File(
            original_file_name=file_name,
            file_name=file_generate_name(file_name),
            file_type=file_type,
            uploaded_by=self.user,
            file=None
        )
        file.full_clean()
        file.save()

        upload_path = file_generate_upload_path(file, file.file_name)

        """
        We are doing this in order to have an associated file for the field.
        """
        file.file = file.file.field.attr_class(file, file.file.field, upload_path)
        file.save()

        presigned_data: Dict[str, Any] = {}

        if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.S3:
            presigned_data = s3_generate_presigned_post(
                file_path=upload_path, file_type=file.file_type
            )

        else:
            presigned_data = {
                "url": file_generate_local_upload_url(file_id=str(file.id)),
            }

        return {"id": file.id, **presigned_data}

    @transaction.atomic
    def finish(self, *, file: File) -> File:
        # Potentially, check against user
        file.upload_finished_at = timezone.now()
        file.full_clean()
        file.save()

        return file
```

### 命名规则

命名约定因人而异。在项目中保持一致的命名约定可以提高代码的可读性和可维护性

如果我们以上面的示例为例，我们的服务名为 `user_create`。这个模式是`<实体>_<操作>`

它具有一些好处：

1. **命名空间**。很容易看出所有以 `user_` 开头的服务，并且将它们放在 `users.py` 模块中是一个好主意
2. **查找性**。换句话说，如果您想查看特定实体的所有操作，只需使用 grep 命令查找 `user_` 字符串即可

### 模块

如果有一个足够简单的 Django 应用程序，其中有许多服务，它们可以全部放在 `services.py` 模块中，很好地运作。

但是，当应用程序变得庞大时，您可能想将 `services.py` 拆分成一个文件夹，其中包含子模块，这取决于您在应用程序中处理的不同子域。

例如，假设我们有一个 `authentication` 应用程序，在我们的 `services` 模块中有 1 个子模块用于处理  `jwt`，另一个子模块用于处理 `oauth`

结构可能如下所示：

```markdown
services
├── __init__.py
├── jwt.py
└── oauth.py
```

有很多种结构的实现方法：

* 在 `services/__init__.py` 中执行导入和导出操作，这样就可以在其他任何地方从 `project.authentication.services` 导入
* 创建文件夹模块，如：`jwt/__init__.py` 并在其中放置代码
* 基本上，结构取决于个人。如何你感觉需要重新组织和重构的话

### 选择器

在我们大多数项目中，我们是区分 `Pushing data to the database` 和 `Pulling data fromthe database`

1. services 负责推送数据到数据库
2. selector 负责从数据库拉取数据
3. selector 可以作为 services 的“子层”，专门负责获取数据

> 如果您对这个想法不太认同，您也可以将服务用于两种类型的操作

selector 遵循与 services 相同的规则

例如，在模块 `<your_app>/selectors.py` 中，我们可以有以下内容：

```python
def user_list(*, fetched_by: User) -> Iterable[User]:
    user_ids = user_get_visible_for(user=fetched_by)

    query = Q(id__in=user_ids)

    return User.objects.filter(query)
```

正如您所看到的，`user_get_visible_for` 是另一个选择器。你可以返回查询集、列表或适合您特定情况的任何东西。

### 测试

由于 `services` 承载我们的业务逻辑，它们是进行测试的理想选择

如果决定用测试覆盖服务层，我们有一些一般性的规则需要遵循：

1. 测试**应该尽可能的覆盖业务逻辑**
2. 测试**应该命中数据库**，创建和读取其中的数据
3. 测试**应该模拟异步任务调用和所有超出项目范围的操作**

创建所需的测试状态时，可以使用以下组合：

* 伪造数据（我们推荐使用 faker）
* 其他服务，用于创建所需的对象。
* 特殊测试工具和辅助方法。
* Factories（我们推荐使用 factory_boy）
* 如果项目中尚未引入工厂，则可以使用 Model.objects.create() 方法。
* 通常采用适合您的方法。

**让我们来看一下上面示例中的服务：**

```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction

from project.payments.selectors import items_get_for_user
from project.payments.models import Item, Payment
from project.payments.tasks import payment_charge


@transaction.atomic
def item_buy(
    *,
    item: Item,
    user: User,
) -> Payment:
    if item in items_get_for_user(user=user):
        raise ValidationError(f'Item {item} already in {user} items.')

    payment = Payment(
        item=item,
        user=user,
        successful=False
    )
    payment.full_clean()
    payment.save()

    # Run the task once the transaction has commited,
    # guaranteeing the object has been created.
    transaction.on_commit(
        lambda: payment_charge.delay(payment_id=payment.id)
    )

    return payment
```

这个服务

* 调用一个 selector 进行验证
* 创建一个对象
* 延时一个任务

下面是测试用例：

```python
from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from django_styleguide.payments.services import item_buy
from django_styleguide.payments.models import Payment, Item


class ItemBuyTests(TestCase):
    @patch('project.payments.services.items_get_for_user')
    def test_buying_item_that_is_already_bought_fails(self, items_get_for_user_mock):
        """
        Since we already have tests for `items_get_for_user`,
        we can safely mock it here and give it a proper return value.
        """
        user = User(username='Test User')
        item = Item(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        items_get_for_user_mock.return_value = [item]

        with self.assertRaises(ValidationError):
            item_buy(user=user, item=item)

    @patch('project.payments.services.payment_charge.delay')
    def test_buying_item_creates_a_payment_and_calls_charge_task(
        self,
        payment_charge_mock
    ):
        # How we prepare our tests is a topic for a different discussion
        user = given_a_user(username="Test user")
        item = given_a_item(
            name='Test Item',
            description='Test Item description',
            price=10.15
        )

        self.assertEqual(0, Payment.objects.count())

        payment = item_buy(user=user, item=item)

        self.assertEqual(1, Payment.objects.count())
        self.assertEqual(payment, Payment.objects.first())

        self.assertFalse(payment.successful)

        payment_charge_mock.assert_called()
```

## API和序列化

当使用 `services` 和 `selectors` 时，你的所有 API 应该看起来简单并且相同

**在创建新的 API 时，我们遵循以下一般性规则：**

* 每个操作只有一个 API，这意味着对于一个模型的 CRUD，需要有四个 API
* 从最简单的 `APIView` 或 `GenericAPIView` 中继承
  * 避免使用更抽象的类，我们希望通过 `services` 和 `selectors` 来管理事物，而不是通过序列化来管理
* **不要在 API 中处理业务逻辑**
* 您可以在 API 中进行**对象获取/数据操作**（可能，你会将它提取到其它地方）
  * 如果你在 API 中调用了 `some_service` ，您可以将对象获取/数据操作提取到 `some_service_parse`
* 基本上，尽可能保持 API 简单。它们是指向核心业务逻辑的接口

当我们谈论 API 时，我们需要一种处理数据序列化的方式，包括传入和传出的数据

**以下是我们的 API 序列化规则：**

* 应该有一个专门的输入序列化和一个专门的输出序列化
* 输入序列化负责传入的数据
* 输出序列化负责传出的数据
* 在序列化方面，使用任何适合你的抽象

**如果使用 DRF 的序列化程序，以下是我们的规则：**

* 序列化应嵌套在 API 中，并命名为 `InputSerializer` 或 `OutputSerializer`
* 我们更喜欢两个序列化程序都继承自更简单的 `Serializer`，而避免使用 `ModelSerializer`
* 如果需要嵌套序列化，请使用 `inline_serializer` 工具
  * 这是个人的喜好和选择问题，如果 `ModelSerializer` 对你有效，请使用它
* 尽可能少地重用序列化器
  * 重用序列化器可能会使您面临意外行为，当基本序列化器发生变化时

### 命名规则

我们在 API 中使用以下命名规则：`<Entity><Action>Api`

示例： `UserCreateApi`, `UserSendResetPasswordApi`, `UserDeactivateApi` 等等...

### 基础类和基础函数

> 这主要取决于个人偏好，因为两种方法都可以实现相同的结果

我们有以下偏好：

1. 默认情况下选择基于类的 API  视图
2. 如果其他人更喜欢和习惯于使用函数，则使用基于函数的 API  视图

对于我们而言，使用基于类的 API  视图的额外好处包括：

1. 您可以继承 BaseApi 或添加 mixins
   * 如果您使用基于函数的 API  视图，则需要使用装饰器来实现相同的功能
2. 类可以创建一个命名空间，在其中可以嵌套其他属性、方法等
   * 可以通过类属性进行额外的 API 配置
   * 在基于函数的 API  视图的情况下，需要堆叠装饰器来完成相同的事情

使用继承 `BaseApi` 的类的示例：

```python
class SomeApi(BaseApi):
    def get(self, request):
        data = something()

        return Response(data)
```

使用 `base_api` 装饰器的函数示例：

```python
@base_api(["GET"])
def some_api(request):
    data = something()
    return Response(data)
```

### List API

#### Plain

简单的 list API 应该长成这个样子：

```python
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response

from styleguide_example.users.selectors import user_list
from styleguide_example.users.models import BaseUser


class UserListApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        email = serializers.CharField()

    def get(self, request):
        users = user_list()

        data = self.OutputSerializer(users, many=True).data

        return Response(data)
```

这个API默认是公共的，是否认证取决于实际需求

#### Filters + Pagination

因为我们的API从DRF的基础 `APIView` 继承，而筛选和分页是集成到通用视图中的。但是，您可以轻松地添加筛选和分页功能到类视图中，例如在get_queryset方法中使用DRF的过滤器和分页器

1. [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
2. [DRF Pagination](https://www.django-rest-framework.org/api-guide/pagination/)

我们采取以下方法：

1. selectors 负责实际的过滤
2. APIs 负责过滤序列化参数
3. 如果需要 DRF 提供的一些通用分页，则 API 应负责处理此问题
4. 如果需要不同的分页，或者正在自己实现分页，则可以添加一个新的层来处理分页，或者让 selectors 为您处理

**使用DRF提供的分页的示例**

```python
from rest_framework.views import APIView
from rest_framework import serializers

from styleguide_example.api.mixins import ApiErrorsMixin
from styleguide_example.api.pagination import get_paginated_response, LimitOffsetPagination

from styleguide_example.users.selectors import user_list
from styleguide_example.users.models import BaseUser


class UserListApi(ApiErrorsMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        # Important: If we use BooleanField, it will default to False
        is_admin = serializers.NullBooleanField(required=False)
        email = serializers.EmailField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        email = serializers.CharField()
        is_admin = serializers.BooleanField()

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self
        )
```

可以看到这个API，我们可以找到一些关键点：

1. 有一个 `FilterSerializer`，它将处理查询参数。如果我们不在这里做，我们将在其他地方处理它，而DRF序列化程序很擅长这项工作。
2. 我们将过滤器传递给 `user_list` selector
3. 我们使用 `get_paginated_response` 实用程序返回分页响应

让我们来看一下selector：

```python
import django_filters

from styleguide_example.users.models import BaseUser


class BaseUserFilter(django_filters.FilterSet):
    class Meta:
        model = BaseUser
        fields = ('id', 'email', 'is_admin')


def user_list(*, filters=None):
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs
```

正如您所见，我们正在利用强大的 `django-filter` 库

> 👀selector 负责筛选操作。你可以选择其他的筛选库或者工具。但对于大多数情况，django-filter 库已经足够了，`django-filter` 足够强大

最后，让我们来看一下 `get_paginated_response` ：

```python
from rest_framework.response import Response


def get_paginated_response(*, pagination_class, serializer_class, queryset, request, view):
    paginator = pagination_class()

    page = paginator.paginate_queryset(queryset, request, view=view)

    if page is not None:
        serializer = serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = serializer_class(queryset, many=True)

    return Response(data=serializer.data)
```

这基本上是从DRF中提取出来的代码

同样适用于 `LimitOffsetPagination`：

```python
from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination as _LimitOffsetPagination
from rest_framework.response import Response


class LimitOffsetPagination(_LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_data(self, data):
        return OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def get_paginated_response(self, data):
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(OrderedDict([
            ('limit', self.limit),
            ('offset', self.offset),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
```

我们基本上是在逆向工程通用API

> 👀 如果你需要其他分页方式，你可以实现它并以相同的方式使用它。有些情况下，selector 需要处理分页。我们处理这些情况的方式与处理筛选一样

您可以在[**Styleguide Example**](https://github.com/HackSoftware/Styleguide-Example#example-list-api)中找到具有过滤器和分页的示例列表API的代码

### Detail API

这里有一个示例：

```python
class CourseDetailApi(SomeAuthenticationMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        name = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def get(self, request, course_id):
        course = course_get(id=course_id)

        serializer = self.OutputSerializer(course)

        return Response(serializer.data)
```

### Create API

这里有一个示例：

```python
class CourseCreateApi(SomeAuthenticationMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_create(**serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)
```

### Update API

这里有一个示例：

```python
class CourseUpdateApi(SomeAuthenticationMixin, APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(required=False)
        start_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)

    def post(self, request, course_id):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_update(course_id=course_id, **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
```

### 获取对象

当我们的API收到一个 `object_id` 时，会产生一个问题：**我们应该在哪里获取这个对象？**

我们有几个建议：

1. 我们可以将该对象传递给一个序列化器，该序列化器具有 `PrimaryKeyRelatedField`（或 `SlugRelatedField`）字段
2. 我们可以在API中进行某种形式的对象获取，然后将该对象传递给一个service或selector
3. 我们可以将id传递给 services/selector，然后在那里进行对象获取

我们采用哪种方法取决于项目上下文和习惯

通常我们会在 API 层级上使用一个特殊的 `get_object` 工具来获取对象：

```python
def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None
```

这是一个非常基本的工具，它处理了异常并返回None

无论你做什么，请确保保持一致

### 序列化嵌套

如果需要使用嵌套序列化器，可以按照以下方式操作：

```python
class Serializer(serializers.Serializer):
    weeks = inline_serializer(many=True, fields={
        'id': serializers.IntegerField(),
        'number': serializers.IntegerField(),
    })
```

`inline_serializer` 的实现可以在[**这里**](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/utils.py#L34)找到 ，在[Styleguide-Example](https://github.com/HackSoftware/Styleguide-Example) 仓库

### 高级序列化

当 API 的输出结果非常复杂时，有时我们想要优化查询，而优化本身可能也很复杂

在这种情况下，仅使用 `OutputSerializer` 可能会限制我们的选择

在这种情况下，我们可以将输出序列化实现为一个函数，并在其中进行所需的优化，**可以将所有优化放在选择器中，也可以将输出序列化作为函数实现，以便进行优化**

我们拿这个 API 作为示例：

```python
class SomeGenericFeedApi(BaseApi):
    def get(self, request):
        feed = some_feed_get(
            user=request.user,
        )

        data = some_feed_serialize(feed)

        return Response(data)
```

在这种情况下，`some_feed_get` 的职责是返回一个新闻订阅项的列表（可以是ORM对象、可以只是ID，可以是适合您的任何内容）

我们希望对这个 feed 进行复杂的序列化时，最优的方法就是把它放到序列化函数 `some_feed_serialize`

这意味着我们不必在 `some_feed_get` 中进行优化或者预处理

`some_feed_serializer` 示例：

```python
class FeedItemSerializer(serializers.Serializer):
    ... some fields here ...
    calculated_field = serializers.IntegerField(source="_calculated_field")


def some_feed_serialize(feed: List[FeedItem]):
    feed_ids = [feed_item.id for feed_item in feed]

    # Refetch items with more optimizations
    # Based on the relations that are going in
    objects = FeedItem.objects.select_related(
      # ... as complex as you want ...
    ).prefetch_related(
      # ... as complex as you want ...
    ).filter(
      id__in=feed_ids
    ).order_by(
      "-some_timestamp"
    )

    some_cache = get_some_cache(feed_ids)

    result = []

    for feed_item in objects:
        # An example, adding additional fields for the serializer
        # That are based on values outside of our current object
        # This may be some optimization to save queries
        feed_item._calculated_field = some_cache.get(feed_item.id)

        result.append(FeedItemSerializer(feed_item).data)

    return result
```

正如您所看到的，这是一个相当通用的示例，但其想法很简单：

1. 重新获取数据，包括所需的关联和预处理
2. 获取或构建缓存，节省查询和计算
3. 返回 API 响应所需要的结果

即使这被标记为“advanced serialization”，但这种模式确实非常强大，并且可以用于所有序列化

这样的序列化函数通常位于对应 Django 应用程序的 `serializers.py ` 模块中

## Urls

我们通常按照与 API 相同的方式组织 URL，即每个 API 对应一个 URL，也就是说每个 URL 对应一个操作

一般的做法是将来自不同域的 URL 分别放置在自己的 `domain_patterns` 列表中，再将其包含在 `urlpatterns` 中

以下是使用上述 API 的示例：

```python
from django.urls import path, include

from project.education.apis import (
    CourseCreateApi,
    CourseUpdateApi,
    CourseListApi,
    CourseDetailApi,
    CourseSpecificActionApi,
)


course_patterns = [
    path('', CourseListApi.as_view(), name='list'),
    path('<int:course_id>/', CourseDetailApi.as_view(), name='detail'),
    path('create/', CourseCreateApi.as_view(), name='create'),
    path('<int:course_id>/update/', CourseUpdateApi.as_view(), name='update'),
    path(
        '<int:course_id>/specific-action/',
        CourseSpecificActionApi.as_view(),
        name='specific-action'
    ),
]

urlpatterns = [
    path('courses/', include((course_patterns, 'courses'))),
]
```

**将URL分割成这样可以给你额外的灵活性，使你能够将不同的域模式移动到单独的模块中**

特别是对于非常大的项目，在其中经常会在 `urls.py` 中遇到合并冲突

如果你想要看到整个url树结构，你可以不提取你包含的url的特定变量

这是我们项目中的一个例子：[**Django Styleguide Example**](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/files/urls.py)

```python
from django.urls import path, include

from styleguide_example.files.apis import (
    FileDirectUploadApi,

    FilePassThruUploadStartApi,
    FilePassThruUploadFinishApi,
    FilePassThruUploadLocalApi,
)


urlpatterns = [
    path(
        "upload/",
        include(([
            path(
                "direct/",
                FileDirectUploadApi.as_view(),
                name="direct"
            ),
            path(
                "pass-thru/",
                include(([
                    path(
                        "start/",
                        FilePassThruUploadStartApi.as_view(),
                        name="start"
                    ),
                    path(
                        "finish/",
                        FilePassThruUploadFinishApi.as_view(),
                        name="finish"
                    ),
                    path(
                        "local/<str:file_id>/",
                        FilePassThruUploadLocalApi.as_view(),
                        name="local"
                    )
                ], "pass-thru"))
            )
        ], "upload"))
    )
]
```

有些人喜欢第一种方式，有些人喜欢可见的树状结构。这取决于你和你的团队

## 配置

在 Django 的设置方面，我们倾向于遵循 [`cookiecutter-django`](https://github.com/cookiecutter/cookiecutter-django) 的文件夹结构，做出少量的调整

* 我们将 Django 特定的设置与其他设置分开
* 所有设置应该都包含在 `base.py`
  * 不应该只包含 `production.py` 的设置
  * 生产环境的设置应该通过环境便利来控制

[`Styleguide-Example`](https://github.com/HackSoftware/Styleguide-Example) 项目的设置文件夹结构：

```bash
config
├── __init__.py
├── django
│   ├── __init__.py
│   ├── base.py
│   ├── local.py
│   ├── production.py
│   └── test.py
├── settings
│   ├── __init__.py
│   ├── celery.py
│   ├── cors.py
│   ├── sentry.py
│   └── sessions.py
├── urls.py
├── env.py
└── wsgi.py
├── asgi.py
```

`config/django` 放置与 django 相关的设置：

* `base.py` 包含大部分设置内容，同时从 `config/settings` 导入其它设置内容
* `production.py` 从 `base.py` 导入并覆盖指定的设置内容用于生产环境
* `test.py` 从 `base.py` 导入并覆盖指定的设置内容用于测试
  * 这个应该被 `pytest.ini`当做设置模块来使用
* `local.py` 从 `base.py` 导入并覆盖指定的设置内容用于开发环境
  * 如果需要使用它，需要将 `manage.py` 的指向修改为 `local`。 否则默认使用 `base.py`

在 `config/settings` 我们还存放了其他设置：

* Celery configuration
* 3rd party configurations

这为你提供了很好的模块分离

此外，我们通常还有一个 `config/env.py` 包含一下代码：

```python
import environ

env = environ.Env()
```

当我们需要从环境变量中导入一些变量的时候，我们通常使用下面这段代码：

```python
from config.env import env
```

通常我们在 `base.py` 模块的结尾处导入所有的来自 `config/settings` 的设置

```python
from config.settings.cors import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.sentry import *  # noqa
```

### DJANGO_为前缀的环境变量

在很多示例中，你会看到环境变量通常以 DJANGO_ 为前缀。当其他应用程序与你的 Django 应用程序一起运行并从相同的环境读取时，这非常有帮助。

我们只给 DJANGO_SETTINGS_MODULE 和 DJANGO_DEBUG 添加 DJANGO_ 前缀，不给其他变量添加。

**这主要取决于个人喜好。只要确保在这方面保持一致即可**

### 集成

所有内容都应该导入到 `base.py`但有时我们不想为本地开发配置特定的集成，我们使用一下方法：

* 特定集成的设置放置在 `config/settings/some_intergration.py`
* 通常会有一个布尔型的设置叫做  `USE_SOME_INTEGRATION`从环境变量中读取，默认值为 `False`
* 如果该值为 `True`，则继续读取其他设置，并在环境中找不到这些设置时报错

例如，让我们来看一下 `config/settings/sentry.py` ：

```python
from config.env import env

SENTRY_DSN = env('SENTRY_DSN', default='')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    # ... we proceed with sentry settings here ...
    # View the full file here - https://github.com/HackSoftware/Styleguide-Example/blob/master/config/settings/sentry.py
```

### .env文件

在本地创建 `.env` 文件提供值给你的配置是一种很好的办法

 [`django-environ`](https://django-environ.readthedocs.io/en/latest/)提供了一种方式来实现这一点：

```python
# That's in the beginning of base.py

import os

from config.env import env, environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3

env.read_env(os.path.join(BASE_DIR, ".env"))
```

现在你可以在项目根目录下拥有一个 `.env` 文件（非必须的），并在其中放置你配置要用的值

有两件事情值得在这里提一下：

1. 不要将 ` .env `文件放入源代码控制中，因为这会泄漏凭据
2. 可以创建一个 `.env.example` 文件，把所有值都设置为空，这样新加入的开发者可以了解需要哪些值。但不要把` .env `文件放在代码仓库中，因为这会泄露凭据

## 错误和异常处理

> 如果你需要这段代码，请查看 Styleguide-Example 项目 - https://github.com/HackSoftware/Styleguide-Example/blob/master/styleguide_example/api/exception_handlers.py

错误和异常处理是一个广泛的话题，往往具体细节与特定项目有关

因此，我们将把事情分为两部分 - **通用指南**，以及一些**特定的错误处理方法**

**我们的通用指南是**：

1. 解异常处理的工作原理（我们将为 Django Rest Framework 提供上下文）
2. 描述您的API错误将是什么样子
3. 解如何更改默认的异常处理行为

**一些具体的方法：**

1. 使用DRF的默认异常，尽可能少的进行修改
2. HackSoft提出的方法

### DRF中异常处理的工作原理

DRF有一个非常好的指南，介绍了异常如何处理，请确保首先阅读它 - https://www.django-rest-framework.org/api-guide/exceptions/

另外，在这里有一个简洁的图表，概述了这个过程：

![Exception handler (1)](https://user-images.githubusercontent.com/387867/142426205-2c0356e6-ce20-425e-a811-072c3334edb0.png)

基本上，如果异常处理程序无法处理给定的异常然后返回 None，结果就是返回一个未处理的异常和 500 服务器错误。这通常是好的，因为你一般不会屏蔽需要关注的错误

**我们需要注意一些细节**

#### DRF中 的ValidationError

例如，如果我们像这样简单地引发 `rest_framework.exceptions.ValidationError`

```python
from rest_framework import exceptions


def some_service():
    raise ValidationError("Error message here.")
```

响应结果将如下所示：

```json
["Some message"]
```

这看起来很奇怪，因为如果我们这样做：

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.ValidationError({"error": "Some message"})
```

响应将如下所示

```json
{
  "error": "Some message"
}
```

那基本上就是我们作为 ValidationError 的 `detail` 传递的内容。但它是一个与最初数组不同的数据结构

如果我们决定抛出 DRF 中的另一个内置异常：

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.NotFound()
```

响应将会像这样：

```json
{
  "detail": "Not found."
}
```

这与我们从 `ValidationError` 看到的行为完全不同，可能会引起问题

以下是DRF默认行为可以为我们提供的内容:

* 数字
* 字典
* 特定的结果：`{"detail": "something"}`

**如果我们需要使用DRF的默认行为，我们需要注意这种不一致性**

#### Django中的ValidationError

DRF的默认异常处理与Django的ValidationError不兼容

这段代码：

```python
from django.core.exceptions import ValidationError as DjangoValidationError


def some_service():
    raise DjangoValidationError("Some error message")
```

这段代码将导致未处理的异常，进而导致 `500 Server Error`

这也会发生在模型验证过程中出现的 ValidationError，例如：

```python
def some_service():
    user = BaseUser()
    user.full_clean()  # Throws ValidationError
    user.save()
```

这段代码同样也会导致 `500 Server Error`

如果我们想要像处理 `rest_framework.exceptions.ValidationError` 那样处理它，我们需要编写自己的自定义异常处理器：

```python
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework.views import exception_handler
from rest_framework.serializers import as_serializer_error
from rest_framework import exceptions


def custom_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    return response
```

这基本上是默认实现，其中增加了以下代码片段：

```python
if isinstance(exc, DjangoValidationError):
    exc = exceptions.ValidationError(as_serializer_error(exc))
```

由于我们需要在  `django.core.exceptions.ValidationError` 和 `rest_framework.exceptions.ValidationError` 之间进行映射，因此我们使用DRF的`as_serializer_error` 函数，该函数在序列化器中内部使用

通过这种方式，我们现在可以让Django的ValidationError和DRF的异常处理程序配合得很好了

### API错误描述

这非常重要，应该在任何一个项目中尽早完成

这基本上是统一你的API错误接口 - **错误是如何作为API响应的标准的？**

这是一些特定的项目，你可以借鉴一些流行的API：

* Stripe - https://stripe.com/docs/api/errors

作为示例，我们可能决定我们的错误将如下所示：

* 4xx 和 5xx 状态码用于表示不同类型的错误
* 每个错误将是一个带有单个 `message` 键的字典，其中包含错误消息

```json
{
  "message": "Some error message here"
}
```

这些简单的就足够了：

* `400` 状态码将用于表示验证错误
* `401` 状态码表示认证错误
* `403` 状态码表示权限错误
* `404` 状态码表示资源未找到错误
* `429` 状态码表示请求频率限制错误
* `500` 状态码表示服务器错误（我们需要小心不要在类似 Sentry 的服务中屏蔽引发500的异常并始终报告它）

这取决于您的项目并且具有一定的特殊性。**我们将针对某个特定方法提出类似的建议**

### 如何修改默认的异常处理行为

这也很重要，因为当你决定错误的样子时，你需要实现自定义的异常处理

我们已经在上面的段落中提供了一个例子：讨论了Django的 **ValidationError**

在下面的部分中，我们还将提供其他示例

### 方法1 - 使用DRF的默认异常处理，只需很少的修改

DRF's错误处理方式很好。如果最终结果总是一致的，那将是很好的。这些是我们将要进行的小修改

我们希望最终的错误信息看起来都是这个样子：

```json
{
  "detail": "Some error"
}
```

或者

```json
{
  "detail": ["Some error", "Another error"]
}
```

或者

```json
{
  "detail": { "key": "... some arbitrary nested structure ..." }
}
```

基本上，确保我们始终拥有一个带有 `detail` 键的字典

额外地，我们也想处理 Django 的  `ValidationError`

为了实现这个目标，我们的自定义异常处理程序将如下所示：

```python
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error


def drf_default_with_modifications_exception_handler(exc, ctx):
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    return response
```

我们复制了原来的异常处理器，以便我们可以在之后处理`APIException`（查找 `detail`）

使用代码：

```python
def some_service():
    raise DjangoValidationError("Some error message")
```

响应：

```json
{
  "detail": {
    "non_field_errors": ["Some error message"]
  }
}
```

使用代码：

```python
from django.core.exceptions import PermissionDenied

def some_service():
    raise PermissionDenied()
```

响应：

```json
{
  "detail": "You do not have permission to perform this action."
}
```

使用代码：

```python
from django.http import Http404

def some_service():
    raise Http404()
```

响应：

```json
{
  "detail": "Not found."
}
```

使用代码：

```python
def some_service():
    raise RestValidationError("Some error message")
```

响应：

```json
{
  "detail": ["Some error message"]
}
```

使用代码：

```python
def some_service():
    raise RestValidationError(detail={"error": "Some error message"})
```

响应：

```json
{
  "detail": {
    "error": "Some error message"
  }
}
```

使用代码：

```python
class NestedSerializer(serializers.Serializer):
    bar = serializers.CharField()


class PlainSerializer(serializers.Serializer):
    foo = serializers.CharField()
    email = serializers.EmailField(min_length=200)

    nested = NestedSerializer()


def some_service():
    serializer = PlainSerializer(data={
        "email": "foo",
        "nested": {}
    })
    serializer.is_valid(raise_exception=True)

```

响应：

```json
{
  "detail": {
    "foo": ["This field is required."],
    "email": [
      "Ensure this field has at least 200 characters.",
      "Enter a valid email address."
    ],
    "nested": {
      "bar": ["This field is required."]
    }
  }
}
```

使用代码：

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.Throttled()
```

响应：

```json
{
  "detail": "Request was throttled."
}
```

使用代码：

```python
def some_service():
    user = BaseUser()
    user.full_clean()
```

响应：

```json
{
  "detail": {
    "password": ["This field cannot be blank."],
    "email": ["This field cannot be blank."]
  }
}
```

### 方法2 - HackSoft's推荐的方法

我们提出了一个方法，可以轻松地扩展为适合你的工作方式

**关键思路：**

 	1.	**你的应用程序将具有其自己的异常层次结构**，由业务逻辑引发异常
 	2.	简单起见，我们假设我们只有1个错误-`ApplicationError`
 	 * 在一个特殊的`核心`应用程序中定义，在`exceptions`模块中。 基本上，是 `project.core.exceptions.ApplicationError`
 	3.	我们希望DRF默认情况下处理所有其他内容
 	4.	`ValidationError `现在很特别，将以不同的方式处理
 	 * `ValidationError` 只能来自于序列化器或模型验证

**我们将为我们的错误定义以下结构：**

```json
{
  "message": "The error message here",
  "extra": {}
}
```

`extra` 键可以保存任意数据，用于向前端传递信息

例如，每当我们遇到 `ValidationError`（通常来自 `Serializer` 或 `Model`）时，我们将呈现如下错误：

```json
{
  "message": "Validation error.",
  "extra": {
    "fields": {
      "password": ["This field cannot be blank."],
      "email": ["This field cannot be blank."]
    }
  }
}
```

这可以与前端进行通信，以便他们查找 `extra.fields`，以将这些特定错误返回给用户

为了实现这一点，自定义异常处理程序将如下所示：

```python
from django.core.exceptions import ValidationError as DjangoValidationError, PermissionDenied
from django.http import Http404

from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.serializers import as_serializer_error
from rest_framework.response import Response

from styleguide_example.core.exceptions import ApplicationError


def hacksoft_proposed_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {
                "message": exc.message,
                "extra": exc.extra
            }
            return Response(data, status=400)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {
            "detail": response.data
        }

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {
            "fields": response.data["detail"]
        }
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response
```

请看一下这段代码，并试着理解其中的含义。**策略是尽可能地重用 DRF 的内容，然后进行调整**

现在，我们将会有以下行为：

代码：

```python
from styleguide_example.core.exceptions import ApplicationError


def trigger_application_error():
    raise ApplicationError(message="Something is not correct", extra={"type": "RANDOM"})
```

响应：

```json
{
  "message": "Something is not correct",
  "extra": {
    "type": "RANDOM"
  }
}
```

代码：

```python
def some_service():
    raise DjangoValidationError("Some error message")
```

响应：

```json
{
  "message": "Validation error",
  "extra": {
    "fields": {
      "non_field_errors": ["Some error message"]
    }
  }
}
```

代码：

```python
from django.core.exceptions import PermissionDenied

def some_service():
    raise PermissionDenied()
```

响应：

```json
{
  "message": "You do not have permission to perform this action.",
  "extra": {}
}
```

代码：

```python
from django.http import Http404

def some_service():
    raise Http404()
```

响应：

```json
{
  "message": "Not found.",
  "extra": {}
}
```

代码：

```python
def some_service():
    raise RestValidationError("Some error message")
```

响应：

```json
{
  "message": "Validation error",
  "extra": {
    "fields": ["Some error message"]
  }
}
```

代码：

```python
class NestedSerializer(serializers.Serializer):
    bar = serializers.CharField()


class PlainSerializer(serializers.Serializer):
    foo = serializers.CharField()
    email = serializers.EmailField(min_length=200)

    nested = NestedSerializer()


def some_service():
    serializer = PlainSerializer(data={
        "email": "foo",
        "nested": {}
    })
    serializer.is_valid(raise_exception=True)

```

响应：

```json
{
  "message": "Validation error",
  "extra": {
    "fields": {
      "foo": ["This field is required."],
      "email": [
        "Ensure this field has at least 200 characters.",
        "Enter a valid email address."
      ],
      "nested": {
        "bar": ["This field is required."]
      }
    }
  }
}
```

代码：

```python
from rest_framework import exceptions


def some_service():
    raise exceptions.Throttled()
```

响应：

```json
{
  "message": "Request was throttled.",
  "extra": {}
}
```

代码：

```python
def some_service():
    user = BaseUser()
    user.full_clean()
```

响应：

```json
{
  "message": "Validation error",
  "extra": {
    "fields": {
      "password": ["This field cannot be blank."],
      "email": ["This field cannot be blank."]
    }
  }
}
```

现在，可以扩展并进行更好的适应以满足你的需求

1. 您可以拥有 `ApplicationValidationError` 和 `ApplicationPermissionError`，作为额外的层级结构
2. 你可以重新实现 DRF 的默认异常处理程序，而不是重用它（复制粘贴并根据自己的需求进行调整）

**总体思路是 - 确定您需要哪种错误处理方式，然后相应地进行实现**

### 更多想法

正如你所看到的，我们可以根据我们的需求来定制异常处理

你甚至可以开始处理更多的东西 - 例如，将 `django.core.exceptions.ObjectDoesNotExist`  转换成 `rest_framework.exceptions.NotFound`

你甚至可以处理所有的异常，但是你必须确保这些异常被正确记录日志，否则你可能会忽略一些重要的问题

## 测试

概述

测试是一个有趣而广泛的话题

你可以听听 [Radoslav Georgiev's talk at DjangoCon Europe 2022](https://www.youtube.com/watch?v=PChaEAIsQls)

![Quality Assurance in Django - Testing what matters](https://camo.githubusercontent.com/28d12ceb7da766568505521c36dad2acfd6ad36d8a39d322c8da8d332568163f/68747470733a2f2f696d672e796f75747562652e636f6d2f76692f5043686145414973516c732f302e6a7067)

在我们的Django项目中，我们根据它们所代表的代码类型来分别测试

这意味着，我们通常有针对模型、services、selectors 和 API/视图的测试

文件结构通常如下：

```bash
project_name
├── app_name
│   ├── __init__.py
│   └── tests
│       ├── __init__.py
│       ├── factories.py
│       ├── models
│       │   └── __init__.py
│       │   └── test_some_model_name.py
│       ├── selectors
│       │   └── __init__.py
│       │   └── test_some_selector_name.py
│       └── services
│           ├── __init__.py
│           └── test_some_service_name.py
└── __init__.py
```

### 命名规则

我们遵循两种常规命名规则：

1. 测试文件名称应为 `test_the_name_of_the_thing_that_is_tested.py`
2. 测试用例应该是类 `TheNameOfTheThingThatIsTestedTests（TestCase）`

举个例子，如果我们有以下的 services：

```python
def a_very_neat_service(*args, **kwargs):
    pass
```

我们的文件名将会是这样的：

```bash
project_name/app_name/tests/services/test_a_very_neat_service.py
```

以及测试用例

```python
class AVeryNeatServiceTests(TestCase):
    pass
  
```

对于工具类的函数测试，我们遵循以下规则：

例如，如果我们有`project_name/common/utils.py`，那么我们将会有`project_name/common/tests/test_utils.py`并在该文件中放置不同的测试用例

如果我们要将utils.py模块拆分为子模块，那么测试也会遵循相同的方式

* `project_name/common/utils/files.py`
* `project_name/common/tests/utils/test_files.py`

我们尽量使我们模块的结构与相应测试的结构相匹配

### 数据工厂

Factories 是用于为测试生成数据的好工具

正确使用时，可以提高测试的整体质量

如果您对这个概念还不熟悉，可以参考以下资料：

* [Improve your Django tests with fakes and factories](https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories)
* https://www.hacksoft.io/blog/improve-your-tests-django-fakes-and-factories-advanced-usage
* [DjangoCon 2022 | factory_boy: testing like a pro](https://www.youtube.com/watch?v=-C-XNHAJF-c)

## Celery

我们通常使用Celery来处理以下几种情况：

* 与第三方服务通信（发送电子邮件、通知等）
* 在HTTP循环之外处理更重的计算任务
* 定期任务（使用Celery beat）

### 基础

我们尝试将Celery视为我们核心逻辑的另一个接口，**不要将业务逻辑放在其中**

让我们来看一个发送电子邮件的服务的示例（示例来自 [`Django-Styleguide-Example`](https://github.com/HackSoftware/Django-Styleguide)）

```python
from django.db import transaction
from django.core.mail import EmailMultiAlternatives

from styleguide_example.core.exceptions import ApplicationError
from styleguide_example.common.services import model_update
from styleguide_example.emails.models import Email


@transaction.atomic
def email_send(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready emails. Current status is {email.status}")

    subject = email.subject
    from_email = "styleguide-example@hacksoft.io"
    to = email.to

    html = email.html
    plain_text = email.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email, _ = model_update(
        instance=email,
        fields=["status", "sent_at"],
        data={
            "status": Email.Status.SENT,
            "sent_at": timezone.now()
        }
    )
    return email
```

发送电子邮件具有业务逻辑，但我们仍然希望从任务中触发此特定服务

我们的任务代码如下：

```python
from celery import shared_task

from styleguide_example.emails.models import Email


@shared_task
def email_send(email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send
    email_send(email)
```

正如你所看到的，我们将任务当做一个 API

* 获取所需数据
* 调用相应的服务

现在，想象一下我们有一个不同的服务，它触发电子邮件发送

它可能是这样的：

```python
from django.db import transaction

# ... more imports here ...

from styleguide_example.emails.tasks import email_send as email_send_task


@transaction.atomic
def user_complete_onboarding(user: User) -> User:
    # ... some code here

    email = email_get_onboarding_template(user=user)

    transaction.on_commit(lambda: email_send_task.delay(email.id))

    return user
```

这里有两个重要的事情需要指出：

1. 我们正在导入任务（与服务名称相同），但是我们给它加上了 `_task`后缀
2. 当事务提交时，我们将调用该任务

**因此，一般来说，我们使用 Celery 的方式可以描述为：**

1. 任务调用services
2. 我们在任务的函数体中导入services
3. 当我们想要触发任务时，我们在模块级别导入该任务，并给它加上 `_task` 后缀
4. 我们通过事务提交时来执行任务

将任务和服务混合使用的这种方式还可以**避免循环导入**的问题，使用 Celery 时这种情况可能会发生

### 错误处理

有时，我们的服务可能会失败，我们可能希望在任务级别处理错误。例如，我们可能想要重试该任务

这种错误处理代码需要存在于任务中

让我们通过添加错误处理来扩展上面的 `email_send` 任务示例：

```python
from celery import shared_task
from celery.utils.log import get_task_logger

from styleguide_example.emails.models import Email


logger = get_task_logger(__name__)


def _email_send_failure(self, exc, task_id, args, kwargs, einfo):
    email_id = args[0]
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_failed

    email_failed(email)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self, email_id):
    email = Email.objects.get(id=email_id)

    from styleguide_example.emails.services import email_send

    try:
        email_send(email)
    except Exception as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)
```

正如你所看到的，我们进行了多次重试，如果所有重试都失败了，我们将在 on_failure 回调函数中处理这种情况

回调函数遵循 `_{task_name}_failure` 命名规则，并像普通任务一样调用服务层

### 配置

我们基本上遵循了与 Django 集成 Celery 的官方指南 - https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html

要查看完整的示例，您可以检查 `Django-Styleguide-Example` 项目中的 Celery 配置

* https://github.com/HackSoftware/Django-Styleguide-Example/tree/master/styleguide_example/tasks
* https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/tasks/celery.py

Celery 是一个复杂的主题，因此花时间阅读文档并了解不同的配置选项是一个好主意

我们经常这样做并发现新的事物或找到更好的方法来解决问题

### 结构

任务位于不同应用程序的 `tasks.py` 模块中

我们遵循与其他所有内容（API、services、selector）相同的规则：**如果给定应用程序的任务变得过于庞大，请按域拆分它们**

也就是说，您最终可以得到 `tasks/domain_a.py` 和 `tasks/domain_b.py` 只需要在 `tasks/init.py` 中导入它们，Celery 就会自动发现它们

一般的经验法则是，按照让自己感觉合理的方式拆分任务

### 定时任务

管理定期任务非常重要，特别是当您有几十个或几百个任务时

我们使用 [Celery Beat](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) + `django_celery_beat.schedulers:DatabaseScheduler` + [`django-celery-beat`](https://github.com/celery/django-celery-beat) 来管理我们的定期任务

我们额外的编写一个管理命令工具 [`setup_periodic_tasks`](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/tasks/management/commands/setup_periodic_tasks.py) 包含系统中所有定期任务的定义。该命令位于上面讨论的 `tasks` 应用程序中

以下是 `project.tasks.management.commands.setup_periodic_tasks.py` 的代码示例

```python
from django.core.management.base import BaseCommand
from django.db import transaction

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask

from project.app.tasks import some_periodic_task


class Command(BaseCommand):
    help = f"""
    Setup celery beat periodic tasks.

    Following tasks will be created:

    - {some_periodic_task.name}
    """

    @transaction.atomic
    def handle(self, *args, **kwargs):
        print('Deleting all periodic tasks and schedules...\n')

        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks_data = [
            {
                'task': some_periodic_task
                'name': 'Do some peridoic stuff',
                # https://crontab.guru/#15_*_*_*_*
                'cron': {
                    'minute': '15',
                    'hour': '*',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True
            },
        ]

        for periodic_task in periodic_tasks_data:
            print(f'Setting up {periodic_task["task"].name}')

            cron = CrontabSchedule.objects.create(
                **periodic_task['cron']
            )

            PeriodicTask.objects.create(
                name=periodic_task['name'],
                task=periodic_task['task'].name,
                crontab=cron,
                enabled=periodic_task['enabled']
            )
```

几个关键点：

* 我们将此任务作为部署过程的一部分使用
* 我们总是在任务中放置一个 [`crontab.guru`](https://crontab.guru/) 的链接以解释 Cron 表达式。否则，表达式将难以理解
* 所有东西都在一个地方
* ⚠️ 我们几乎完全使用 Cron 表达式作为调度周期。如果您计划使用 Celery 提供的其他调度周期对象，请仔细阅读它们的文档以及有关指向相同调度周期对象的重要说明（[https://django-celery-beat.readthedocs.io/en/latest/#example-creating-interval-based-periodic-task）](https://django-celery-beat.readthedocs.io/en/latest/#example-creating-interval-based-periodic-task）

### 其它

Celery 提供了强大的工具来实现复杂的工作流程 - https://docs.celeryq.dev/en/stable/userguide/canvas.html

如果你决定使用它们，规则仍然有效

可能需要稍微重新组织一下，但只要你有一个明确定义的与应用程序核心交互的接口，就可以在更复杂的场景中混合匹配任务和服务

更复杂的场景取决于其上下文。确保你了解架构和你正在做出的决策

## Cookbook

一些通用可重用代码实现存储在这里

### 服务更新

关于更新，我们有一个通用的更新服务，我们在实际更新服务中使用它。以下是示例 `user_update` 服务的代码：

```python
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = ['first_name', 'last_name']

    user, has_updated = model_update(
        instance=user,
        fields=non_side_effect_fields,
        data=data
    )

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
```

* 对于没有与其相关的影响（即它们仅被设置为我们提供的值）的字段，我们调用通用的 `model_update` 服务
* 这种模式允许我们从通用服务中提取重复的字段设置，并在更新服务中仅执行特定任务
* 我们可以使用 `update_fields` 参数进行智能操作，在保存实例时提供此参数。这样，在 `UPDATE` 查询中，我们只会发送实际更新的值

这些服务的完整实现可以在我们的示例项目中找到：

* [`model_update`](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/services.py)
* [`user_update`](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/users/services.py)

如果你将 `model_update` 包含在你的项目中，确保 [read the tests](https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/tests/services/test_model_update.py) 也同样包含在内

## 开发者经验

以下是一些可以让你的 Django 开发尽力更轻松的技巧和工具

### mypy-类型注解

关于使用类型注释以及 `mypy`，[这个推文](https://twitter.com/queroumavodka/status/1294789817071542272)与我们的理念非常相似：

* 我们有一些项目，我们强制执行 `mypy` 并对此非常严格
* 们有一些项目，类型定义相对宽松，而且根本不使用 `mypy`

这里的上下文才是王道

在 [`Django-Styleguide-Example`](https://github.com/HackSoftware/Django-Styleguide-Example) 中我们使用 https://github.com/typeddjango/django-stubs 和 https://github.com/typeddjango/djangorestframework-stubs/ 配置了 `mypy`  ，你可以把它当做一个示例来查看

此外，这个特定的项目 https://github.com/wemake-services/wemake-django-template 也有 mypy 配置

## 其它 Django 风格指南

这里收集了不同的人和公司，发现风格他们的风格指南很有用

**Michael Valencia, CTO at [Facturedo](https://facturedo.com/)**

> 在 Facturedo 的核心项目中，源代码变得杂乱无章。业务逻辑分散在许多不连贯的地方。我们需要一种解决方案来构建 Django 项目的结构，并在 Django Styleguide 中找到了它。
>
> 我们建议任何想要构建中型到大型项目结构的人都使用该指南。它是一个明确定义且不断发展的指南

## 其它资源/替代方案

下是我们发现有用并且可以为风格指南增添价值的其他资源和替代方案

* [Dan Palmer - Scaling Django to 500 apps (DjangoCon US 2021)](https://www.youtube.com/watch?v=NsHo-kThlqI)

* [Django API Domains](https://phalt.github.io/django-api-domains/)
* [A YC News discussion around the Django Styleguide](https://news.ycombinator.com/item?id=34337667) 您可能在这里找到其他有用的资源

## 灵感

我们做 Django 的方式受到以下事物的启发：

* **分离关注点**的大概想法
* [Boundaries by Gary Bernhardt](https://www.youtube.com/watch?v=yTkzNHF6rMs)

* Rails service objects

