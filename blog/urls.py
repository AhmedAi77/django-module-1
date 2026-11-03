from django.urls import path
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.post import PostViewSet, get_posts
from .views.user import create_user
from .views.category import category
from .views.comment import comment


router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('posts/get_post/', get_posts, name='get_post'),
    path('users/', create_user, name='create_user'),
    path('categories/', category, name='category'),
    path('comments/', comment, name='comment'),
]
urlpatterns +=router.urls

