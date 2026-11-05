# Django Blog Project 

## 1. Project Architecture

Django is a Python web framework used to build backend applications.

Django REST Framework (DRF) extends Django with tools for building REST APIs.

The main request flow is:

```text
Client / Postman
       ↓
URL Router
       ↓
API View
       ↓
Serializer / Service
       ↓
Model / ORM
       ↓
PostgreSQL Database
```

The exact flow depends on the operation. Creating a user uses a serializer, while summarizing a post uses a service that retrieves database content and communicates with AI.

### Important components

| Component | Responsibility |
|---|---|
| `settings.py` | Project configuration |
| `urls.py` | Maps URLs to views |
| Model | Defines database structure |
| ORM | Performs database operations using Python |
| Serializer | Validates and converts API data |
| View | Handles HTTP requests and responses |
| Service | Contains reusable application logic |
| AI Client | Communicates with the external AI provider |

**Key idea:** Each component should have a clear responsibility.

---

## 2. Django Project Structure

```text
Module1/
├── manage.py
├── config/
│   ├── settings.py
│   └── urls.py
└── blog/
    ├── models/
    ├── serializers/
    ├── views/
    ├── ai_content/
    │   ├── client.py
    │   └── service/
    │       ├── utils.py
    │       ├── generate.py
    │       └── summarizer.py
    └── urls.py
```

`config` contains the project-wide configuration.

`blog` contains the application functionality.

`manage.py` is used to execute Django commands such as running the development server, applying migrations, and opening the Django shell.

## 3. URL Routing

Django uses URL patterns to decide which view handles a request.

In `config/urls.py`:

```python
path("blog/", include("blog.urls"))
```

This forwards requests beginning with `/blog/` to the blog application's URLs.

In `blog/urls.py`:

```python
path(
    "posts/<int:post_id>/summarize/",
    summarize_post_view,
    name="summarize_post"
)
```

The full URL becomes:

```text
/blog/posts/3/summarize/
```

### Syntax breakdown

- `path()` registers a URL pattern.
- `<int:post_id>` captures an integer from the URL.
- `summarize_post_view` identifies the function Django calls.
- `name=` gives the URL a reusable internal name.
- `include()` delegates routing to another URL configuration.

Django passes the captured ID to the view:

```python
def summarize_post_view(request, post_id):
```

**Remember:** The URL determines where the request goes. It does not perform database operations itself.

---

## 4. Django Models

A model is a Python class that describes database records.

```python
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
```

### Understanding the syntax

`class Category` defines a Python class.

`models.Model` is the Django base class that provides model functionality.

`name` and `description` are model fields.

Django uses model definitions and migrations to create database tables.

### Common fields

| Field | Purpose |
|---|---|
| `CharField` | Short text |
| `TextField` | Long text |
| `EmailField` | Email-format validation |
| `AutoField` | Automatically generated integer ID |
| `DateTimeField` | Date and time |
| `ForeignKey` | Many-to-one relationship |
| `ManyToManyField` | Many-to-many relationship |

### Field options

```python
unique=True
```

Prevents duplicate values at the database level.

```python
blank=True
```

Allows empty values during Django validation.

```python
null=True
```

Allows the database to store `NULL`.

```python
auto_now_add=True
```

Sets the creation timestamp.

```python
auto_now=True
```

Updates the timestamp when the object is saved.

---

## 5. Model Relationships

### ForeignKey — One-to-many

```python
author = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="posts"
)
```

One user can write many posts. Each post references one user.

`on_delete=models.CASCADE` tells Django to delete related posts when their referenced user is deleted.

`related_name="posts"` allows reverse access:

```python
user.posts.all()
```

This retrieves the user's posts.

### ManyToManyField — Many-to-many

```python
category = models.ManyToManyField(
    Category,
    related_name="posts",
    blank=True
)
```

A post may belong to several categories, and one category may be linked to several posts.

Django manages the relationship through an intermediate table.

### Comments

Comments use ForeignKey relationships to connect to their author and post.

This supports:

```python
post.comments.all()
```

which retrieves comments related to a post.

---

## 6. Django ORM

ORM stands for **Object-Relational Mapper**.

It allows Python code to interact with database records without writing SQL manually.

Examples:

```python
Post.objects.all()
```

Returns a QuerySet representing all posts.

```python
Post.objects.get(pk=3)
```

Retrieves one post whose primary key is `3`.

```python
Post.objects.filter(author=1)
```

Returns posts matching the specified author.

### Understanding `Post.objects.get(pk=post_id)`

- `Post` is the model class.
- `.objects` is the Django model manager.
- `.get()` retrieves one matching object.
- `pk` represents the primary key field.
- `post_id` is the value used for the lookup.

If the record does not exist, Django raises:

```python
Post.DoesNotExist
```

A service can catch that exception and raise a clearer application error.

---

## 7. Migrations

Models describe the desired database structure, but editing a model does not immediately update the database.

Two commands are used:

```bash
python manage.py makemigrations
```

Creates migration files describing model changes.

```bash
python manage.py migrate
```

Applies pending migrations to the database.

### Important distinction

Creating an ordinary database record through an API does not require a new migration.

Changing the model schema generally does.

---

## 8. Serializers

Serializers provide validation and data conversion for APIs.

Example:

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
```

`ModelSerializer` automatically creates serializer fields based on the model.

`class Meta` contains configuration for the serializer.

`fields = "__all__"` means all model fields are included.

### Input validation

```python
serializer = CommentSerializer(data=request.data)
```

Creates a serializer instance containing incoming request data.

```python
serializer.is_valid()
```

Runs validation.

```python
serializer.save()
```

Creates or updates the model instance using validated data.

```python
serializer.data
```

Provides the serialized output representation.

```python
serializer.errors
```

Contains validation errors.

### Custom validation

```python
def validate(self, attrs):
    if not attrs.get("author"):
        raise serializers.ValidationError({
            "author": "This field is required."
        })

    return attrs
```

`validate()` runs object-level validation.

`attrs` contains values that have already passed field-level validation.

`raise` stops normal execution and signals an error.

---

## 9. Django REST Framework Views

Views handle incoming HTTP requests.

```python
@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)
```

### Syntax explanation

`@api_view(["POST"])` is a decorator. It makes the function a DRF view that accepts POST requests.

`request.data` contains parsed request content.

`Response()` builds the HTTP response.

`status=201` indicates successful creation.

`status=400` indicates invalid input.

### HTTP methods

| Method | Purpose |
|---|---|
| GET | Retrieve |
| POST | Create or trigger processing |
| PUT | Full update |
| PATCH | Partial update |
| DELETE | Delete |

---

## 10. ViewSets and Routers

DRF provides `ModelViewSet` to implement standard CRUD operations.

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

`queryset` identifies the records available through the ViewSet.

`serializer_class` specifies the serializer used for input and output.

A router creates standard URLs:

```python
router = DefaultRouter()
router.register("posts", PostViewSet)
```

This supports endpoints such as:

```text
GET    /blog/posts/
POST   /blog/posts/
GET    /blog/posts/3/
PATCH  /blog/posts/3/
DELETE /blog/posts/3/
```

A manual API view provides more control over custom operations. A ViewSet reduces repetitive code for standard CRUD.

---

## 11. Python Syntax Used in the Project

### Function parameters and return types

```python
def summarize_post(post_id: int) -> dict:
```

- `def` defines a function.
- `post_id` is a parameter.
- `: int` is a type hint.
- `-> dict` describes the expected return type.
- `:` starts the function body.

Python does not automatically enforce these type hints.

### Default arguments

```python
def generate(self, prompt, system=None):
```

`system=None` makes the argument optional.

### Dictionary access

```python
post_id = request.data.get("post_id")
```

`.get()` retrieves the value associated with a dictionary key, returning `None` when the key is missing unless another default is specified.

### Strings

```python
prompt = f"Summarize this post:\n{content}"
```

`f` creates a formatted string.

`{content}` inserts the variable's value.

`\n` creates a new line.

### Exceptions

```python
try:
    post = Post.objects.get(pk=post_id)
except Post.DoesNotExist:
    raise ValueError("Post not found.")
```

`try` runs code that may fail.

`except` catches a specified exception.

`raise` raises an exception.

### Cleaning strings

```python
summary.strip()
```

Returns a new string without leading or trailing whitespace.

It does not modify the original string unless the result is assigned.

### Checking empty values

```python
if not summary or not summary.strip():
    raise ValueError("Summary is empty.")
```

The first condition checks for an empty or missing value.

The second detects whitespace-only strings.

`or` means either condition can trigger the error.

---

## 12. AI Client — OpenAI Integration

The AI client is responsible for communicating with OpenAI.

```python
class ContentClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_APIKEY
        )

    def generate(self, prompt, system=None):
        messages = []

        if system:
            messages.append({
                "role": "system",
                "content": system
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages
        )

        return response.choices[0].message.content
```

### Important concepts

`__init__()` is called when a new instance is created.

`self` refers to that instance.

`self.client` stores the configured OpenAI client.

`messages` is a list of dictionaries describing the conversation sent to the model.

`chat.completions.create()` sends the request.

`response.choices[0].message.content` extracts the generated text from the first returned choice.

### Why use one shared client?

The same `ContentClient` can support several AI features.

The client handles communication, while each service decides what task the AI should perform.

---

## 13. AI Blog Generator

The generator takes a title and optional tone, then creates new content.

```python
def _build_generate_prompt(title: str, tone: str = None) -> str:
    prompt = f"Write a short blog post about {title}."

    if tone:
        prompt += f"\nWrite it in a {tone} tone."

    return prompt
```

The generator service:

1. Validates the title.
2. Builds the generation prompt.
3. Calls the AI utility.
4. Cleans the generated content.
5. Enforces the configured output length.
6. Returns structured data.

The generator does not need to retrieve an existing post.

---

## 14. AI Blog Summarizer

The summarizer works differently: it receives an existing `post_id` and summarizes the content saved in PostgreSQL.

### Service workflow

```text
post_id
   ↓
Validate positive integer
   ↓
Retrieve Post using ORM
   ↓
Validate post.content
   ↓
Build summary prompt
   ↓
ContentClient.generate(prompt)
   ↓
Validate AI response
   ↓
Return dictionary
```

### Input validation

```python
if type(post_id) is not int or post_id <= 0:
    raise ValueError("Post ID must be a positive integer.")
```

The ID must be a positive integer.

### Database retrieval

```python
try:
    post = Post.objects.get(pk=post_id)
except Post.DoesNotExist:
    raise ValueError("Post not found.")
```

The service retrieves an existing post and converts the database lookup failure into an application-level error.

### Content validation

```python
cleaned_content = validate_text_input(
    post.content,
    min_length=20,
    field_name="Content"
)

if len(cleaned_content) > 500:
    raise ValueError(
        "Post content must not exceed 500 characters."
    )
```

The original post content must contain between 20 and 500 characters after cleaning.

### AI processing

```python
prompt = summarize_builder(cleaned_content)

client = ContentClient()
summary = client.generate(prompt)
```

The prompt builder creates the instructions.

The AI client sends the instructions to OpenAI.

### Output validation

```python
if not summary or not summary.strip():
    raise ValueError("Summary is empty.")
```

The response must contain meaningful text.

### Dictionary result

```python
summary = summary.strip()

return {
    "post_id": post_id,
    "summary": summary,
    "length": len(summary)
}
```

The service returns a normal Python dictionary, not an HTTP response.

---

## 15. AI Summarizer API Endpoint

Endpoint:

```http
POST /blog/posts/3/summarize/
```

The URL contains `post_id=3`.

The API View receives that ID and passes it to the service:

```python
@api_view(["POST"])
def summarize_post_view(request, post_id):
    try:
        result = summarize_post(post_id)
        return Response(result, status=200)

    except ValueError as exc:
        if str(exc) == "Post not found.":
            return Response(
                {"error": str(exc)},
                status=404
            )

        return Response(
            {"error": str(exc)},
            status=400
        )
```

The View does not retrieve the post directly or call OpenAI itself.

This keeps the service reusable from the Django shell or other Python code.

### Expected responses

| Situation | HTTP status |
|---|---|
| Summary generated | 200 OK |
| Invalid content | 400 Bad Request |
| Post doesn't exist | 404 Not Found |
| Unsupported HTTP method | 405 Method Not Allowed |

The AI service does not save the summary to a database table. Summary storage was outside the task's scope.

---

## 16. Logging and Debugging

Python's `logging` module records diagnostic information.

```python
import logging

logger = logging.getLogger(__name__)
```

`__name__` identifies the current Python module.

Example:

```python
try:
    summary = client.generate(prompt)
except Exception:
    logger.exception(
        "Failed to summarize post %s",
        post_id
    )
    raise
```

`logger.exception()` records the error and traceback.

The final `raise` re-raises the original exception.

This is useful when an external AI request fails, such as an authentication error.

---

## 17. Testing

### Test creating a post

```http
POST /blog/posts/
```

A successful creation generally returns `201 Created`.

### Test summarization

```http
POST /blog/posts/3/summarize/
```

No JSON body is required because the ID is already in the URL.

A valid request returns a generated summary and its character length.

### Test error handling

Check these conditions:

- Negative or zero post ID.
- Nonexistent post ID.
- Content shorter than 20 characters.
- Content longer than 500 characters.
- Empty AI response.
- Invalid AI credentials.

Not every test needs a real OpenAI request. Validation and API behavior can also be tested with mocked AI responses.

---

## 18. Quick Reference

| Concept | Remember |
|---|---|
| Model | Defines database structure |
| ORM | Queries the database with Python |
| Migration | Applies schema changes |
| Serializer | Validates and converts API data |
| View | Handles HTTP requests and responses |
| Service | Contains reusable application logic |
| Client | Communicates with an external API |
| `self` | Current class instance |
| `__init__()` | Initializes an instance |
| `__name__` | Current module name |
| `.get()` | Retrieves a value or record, depending on the object |
| `.strip()` | Removes surrounding whitespace |
| `raise` | Raises an exception |
| `try/except` | Handles exceptions |
| `return` | Sends a value back to the caller |
| `-> dict` | Expected dictionary return type |

## Final Mental Model

For a regular CRUD API:

```text
Request → URL → View → Serializer → Model / ORM → Database
```

For your AI summarizer:

```text
Request → URL → View → Service
                          ↓
                     Database
                          ↓
                     Validation
                          ↓
                     Prompt Builder
                          ↓
                     ContentClient
                          ↓
                       OpenAI
                          ↓
                     Dictionary
                          ↓
                     View → JSON
```

**The most important skill is understanding where each responsibility belongs and how data moves between functions, classes, and layers.**
