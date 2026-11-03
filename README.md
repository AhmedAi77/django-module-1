# Django Blog Project – Simple Review

This project is a Blog Backend built with Django and Django REST Framework.

The main idea is:

```text
Client / Postman
       ↓
URL
       ↓
View
       ↓
Serializer
       ↓
Model
       ↓
Database
```

When returning data:

```text
Database
↓
Model
↓
Serializer
↓
Response / JSON
```

## 1. Project and App

I have a Django project called:

```text
config
```

It contains the main project configuration, such as:

```text
settings.py
urls.py
```

I also have an app called:

```text
blog
```

The `blog` app contains the main blog logic:

```text
models
serializers
views
urls
```

Simple way to remember it:

```text
config = whole-project configuration
blog   = blog feature
```

## 2. settings.py

`settings.py` contains the main Django configuration.

One important section is:

```python
INSTALLED_APPS
```

For example:

```python
'rest_framework',
'blog',
```

`rest_framework` is needed because we are building REST APIs with Django REST Framework.

The project also connects to PostgreSQL.

Sensitive information such as database passwords should not be written directly inside `settings.py`.

Instead, they can be stored in:

```text
.env
```

and loaded using `python-decouple`.

## 3. URLs

There are two URL levels.

The first one is:

```text
config/urls.py
```

This is the main router for the whole Django project.

For example:

```python
path('api/', include('blog.urls'))
```

This means:

> If the URL starts with `/api/`, send the remaining part to `blog/urls.py`.

Then inside `blog/urls.py`, I can have:

```python
path('users/', create_user)
```

So the final URL becomes:

```text
/api/users/
```

Simple way to remember:

```text
config/urls.py
= chooses the app

blog/urls.py
= chooses the view
```

## 4. Models

A Model represents data stored in the database.

For example:

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
```

This represents something similar to:

```text
Category table

id
name
description
```

Django handles the SQL for us through the ORM.

## 5. Models in the project

The project contains:

```text
User
Post
Category
Comment
```

They are organized into separate files:

```text
blog/models/
    user.py
    post.py
    category.py
    comment.py
```

`__init__.py` imports the models so Django can find and use them.

## 6. Common Model Fields

```python
models.CharField(max_length=100)
```

Used for short text such as a username or title.

```python
models.TextField()
```

Used for longer text such as post content or comments.

```python
models.EmailField()
```

Used for email addresses and provides email-format validation.

```python
models.DateTimeField(auto_now_add=True)
```

Stores the creation time.

```python
models.DateTimeField(auto_now=True)
```

Updates the timestamp whenever the object is saved.

```python
unique=True
```

Prevents duplicate values.

For example:

```python
username = models.CharField(
    max_length=100,
    unique=True
)
```

Two users cannot have the same username.

## 7. ForeignKey Relationships

For example, a Post can have an author:

```python
author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='posts'
)
```

This means:

```text
One User
↓
Many Posts
```

Each Post points to one User.

`related_name='posts'` allows:

```python
user.posts.all()
```

which returns the user's posts.

`on_delete=models.CASCADE` means related objects can be deleted when the referenced object is deleted.

For example, deleting a Post can delete its related Comments if the Comment uses `CASCADE`.

## 8. ManyToMany Relationship

A Post can belong to several Categories.

For example:

```python
categories = models.ManyToManyField(
    Category,
    related_name='posts',
    blank=True
)
```

This means:

```text
One Post
→ Many Categories

One Category
→ Many Posts
```

Example:

```text
Post: Django REST Framework

Categories:
Python
Backend
Technology
```

Django creates an intermediate relationship table automatically.

## 9. blank=True and null=True

```python
blank=True
```

Means the field can be empty during validation or in forms.

```python
null=True
```

Means the database is allowed to store:

```text
NULL
```

For a ManyToManyField, normally `blank=True` is enough. `null=True` is not needed.

## 10. Migrations

When I change a Model, the database does not change automatically.

First:

```bash
python manage.py makemigrations
```

This creates migration instructions.

Then:

```bash
python manage.py migrate
```

This applies those changes to the database.

The flow is:

```text
Model change
↓
makemigrations
↓
Migration file
↓
migrate
↓
Database change
```

This matches the course material, which explains migrations as the safe way to apply model/schema changes to the database.

## 11. Django ORM

The Django ORM lets me work with the database using Python instead of writing SQL directly.

For example:

```python
Post.objects.all()
```

means:

```text
Get all Posts
```

And:

```python
Post.objects.get(id=1)
```

means:

```text
Get one Post with id=1
```

Django converts these Python operations into SQL internally.

## 12. Serializer

The Serializer is the layer between the API and the Model.

For example, the client sends:

```json
{
  "content": "Great article",
  "author": 1,
  "post": 2
}
```

The Serializer validates this data before saving it.

Example:

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
```

The flow is:

```text
JSON
↓
Serializer
↓
Validation
↓
Model
```

When returning data:

```text
Model
↓
Serializer
↓
JSON
```

The material describes serializers as the DRF component that converts model/Python objects into API-friendly data and validates incoming JSON.

## 13. Custom Validation

For the Comment API, I added validation so a Comment cannot be created without an author or post.

Example:

```python
def validate(self, data):

    if not data.get("author"):
        raise serializers.ValidationError({
            "author": "This field is required."
        })

    if not data.get("post"):
        raise serializers.ValidationError({
            "post": "This field is required."
        })

    return data
```

If the data is valid:

```text
return data
```

and the Serializer continues.

If the data is invalid:

```text
ValidationError
↓
400 Bad Request
```

## 14. View

The View handles the HTTP request and controls what happens next.

Example:

```python
@api_view(["POST"])
def comment(request):

    serializer = CommentSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

    return Response(
        serializer.errors,
        status=400
    )
```

The logic is:

```text
request.data
↓
Serializer
↓
is_valid()
```

If valid:

```text
save()
↓
Database
↓
201 Created
```

If invalid:

```text
serializer.errors
↓
400 Bad Request
```

The manual-view pattern is also shown in the course material.

## 15. How the Serializer Class Works in the View

This:

```python
class CommentSerializer(
    serializers.ModelSerializer
):
```

defines the Serializer class.

Inside the View:

```python
serializer = CommentSerializer(
    data=request.data
)
```

creates an object, or instance, from that class.

Then:

```python
serializer.is_valid()
```

runs the validation.

This includes the custom:

```python
validate()
```

method.

If validation passes:

```python
serializer.save()
```

saves the object using the Model.

Simple way to remember:

```text
Class
= blueprint

CommentSerializer(...)
= object created from the blueprint

is_valid()
= run validation

validate()
= my custom validation rules

save()
= save through the Model
```

## 16. ViewSet

Not every View needs to be written manually.

Django REST Framework provides:

```python
ModelViewSet
```

Example:

```python
class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()

    serializer_class = PostSerializer
```

A `ModelViewSet` can provide common CRUD operations such as:

```text
GET
POST
PUT
PATCH
DELETE
```

without writing a separate function for every operation.

The course material explains that a ViewSet groups list, retrieve, create, update, and delete operations into one class.

## 17. Router

A Router works with a ViewSet.

Example:

```python
router = DefaultRouter()

router.register(
    'posts',
    PostViewSet
)
```

This can automatically create routes such as:

```text
GET     /api/posts/
POST    /api/posts/

GET     /api/posts/1/
PUT     /api/posts/1/
DELETE  /api/posts/1/
```

Simple way to remember:

```text
ViewSet
= ready CRUD logic

Router
= automatically creates URLs for the ViewSet
```

This matches the material's explanation of ViewSets and Routers.

## 18. Function View vs ViewSet

I use a function-based view such as:

```python
@api_view(["POST"])
def comment(request):
```

when I want more explicit control.

For example:

```text
custom validation
business rules
custom error messages
custom response logic
```

I use a ViewSet when the API mainly needs standard CRUD operations and I want less repeated code.

The course notes explain that manual views give more control, while routers and ViewSets are faster for standard CRUD APIs.

## 19. APIs Built in the Project

The project currently has:

```text
POST /api/users/
```

Creates a User.

```text
POST /api/categories/
```

Creates a Category.

```text
POST /api/posts/
```

Creates a Post.

```text
POST /api/comments/
```

Creates a Comment.

## 20. HTTP Status Codes

Successful creation:

```text
201 Created
```

Invalid input:

```text
400 Bad Request
```

Examples:

```text
duplicate username
invalid email
missing required field
invalid author ID
invalid post ID
```

Unexpected internal server problem:

```text
500 Internal Server Error
```

## 21. The Whole Project in One Flow

If someone asks me how the project works:

```text
Client sends request
↓
URL finds the View
↓
View gives data to Serializer
↓
Serializer validates it
↓
Model / ORM talks to PostgreSQL
↓
Data is saved
↓
Serializer prepares response data
↓
View returns JSON Response
```

The easiest way to remember each layer is:

```text
URL
= Where should the request go?

View
= What should happen with the request?

Serializer
= Is the data valid, and how should it be converted?

Model
= What does the data look like?

ORM
= How do I work with the database using Python?

Database
= Where is the data stored?
```
