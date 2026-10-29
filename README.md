# My Django blog — learning notes

I'm building this project step by step. So far, I created the blog models, connected them, and fixed some import and migration errors.

## Organizing the models

I put each model in its own file inside `blog/models/`:

- `user.py` — user information.
- `post.py` — post title, content, author, and categories.
- `comment.py` — comment content, post, and author.
- `category.py` — category name and description.

`__init__.py` imports these models so Django can find them.

## Fields I used

- `CharField(max_length=100)` — short text with a maximum length, like a title.
- `TextField()` — longer text, like post content.
- `EmailField()` — an email field that checks the format during validation.
- `unique=True` — prevents duplicate values, like two users with the same username.
- `AutoField(primary_key=True)` — an automatically generated ID.
- `auto_now_add=True` — saves the creation time.
- `auto_now=True` — updates the time when the object is saved.
- `__str__()` — shows a readable name for the object, like the post title.

## Relationships

### Users and posts

In `Post`, I used:

```python
author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)
```

One user can write many posts. Each post points to one user, or can have no author with the current settings.

`related_name='posts'` lets me get a user's posts with `user.posts.all()`.

### Comments

In `Comment`, I used foreign keys for `post` and `author`. A post can have many comments, and a user can write many comments.

`on_delete=models.CASCADE` means deleting the linked object also deletes the objects pointing to it. For example, deleting a post deletes its comments.

### Posts and categories

In `Post`, I used:

```python
catagories = models.ManyToManyField(Category, related_name='posts', blank=True)
```

A post can have many categories, and a category can have many posts. This is a many-to-many relationship.

`catagories` is how the field is currently spelled in my code.

## `blank=True` and `null=True`

- `blank=True` — the field can be left empty in a form.
- `null=True` — the database can store no value (`NULL`) for the field.

I used both for optional foreign keys. The comment's `post` and `author` currently allow empty values.

For categories, `blank=True` allows a post to have no categories. A many-to-many field doesn't need `null=True`.

## Import error

I tried:

```python
from models import User, Category
```

It failed because `models` is inside `blog`, not at the project root.

Inside `post.py`, I fixed it with:

```python
from .user import User
from .category import Category
```

The dot means the same package. Adding `__init__.py` doesn't make `models` a top-level package.

## Migration error

When I added the required `author` field, Django asked for a default to fill it for existing comments.

`blank=True` alone didn't help because it doesn't allow `NULL` in the database. I added `null=True` to allow the relationship to be empty.

If I want the author to be required, I need to give existing comments an author instead. A one-off default would be an existing user's ID.

```bash
python manage.py makemigrations
python manage.py migrate
```

`makemigrations` creates the database change instructions. `migrate` applies them.
