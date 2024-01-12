from django.urls import path
from .views import PostListView,PostDetailView,UserPostsListView,CommentListView

urlpatterns = [
    path('posts/',PostListView.as_view(),name='post-list'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('users_posts/<int:user_id>/posts/',UserPostsListView.as_view(),name='user-posts-list'),
    path('posts/<int:post_id>/comments/',CommentListView.as_view(),name='comment_list'),
]
