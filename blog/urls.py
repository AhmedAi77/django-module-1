from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.generate import generate_post
from .views.post import get_posts ,PostViewSet
from .views.user import create_user
from .views.category import category
from .views.comment import comment
from .views.summrizer import summarize_post_view

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path("posts/get_post/", get_posts, name="get_post"),
    path("users/", create_user, name="create_user"),
    path("categories/", category, name="category"),
    path("comments/", comment, name="comment"),
    path("posts/generate/", generate_post, name="generate_post"),
    path("posts/<int:post_id>/summarize/", summarize_post_view, name="summarize_post"),]
urlpatterns +=router.urls

