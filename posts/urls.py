from django.urls import path
from .views import PostListView,PostDetailView,userPostsListView

urlpatterns = [
    path('posts/',PostListView.as_view(),name='post-list'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('users_posts/<int:user_id>/posts/',userPostsListView.as_view(),name='user-posts-list'),
]
