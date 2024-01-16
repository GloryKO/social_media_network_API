from django.urls import path
from .views import PostListView,PostDetailView,UserPostsListView,CommentListView,CommentDetailView,LikeCreateView,DislikeCreateView

urlpatterns = [
    path('',PostListView.as_view(),name='post-list'),
    path('<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('users_posts/<int:user_id>/',UserPostsListView.as_view(),name='user-posts-list'),
    path('<int:post_id>/comments/',CommentListView.as_view(),name='comment-list'),
    path('<int:post_id>/comment/<int:comment_id>',CommentDetailView.as_view(),name='comment-detail'),
    path('<int:post_id>/like/', LikeCreateView.as_view(), name='post-like'),
    path('<int:post_id>/dislike/', DislikeCreateView.as_view(), name='post-dislike'),
]
