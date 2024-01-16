from django.shortcuts import render
from rest_framework import generics,permissions
from . serializers import PostSerializer,CommentSerializer,LikeSerializer,DisLikeSerializer
from . models import Post,Comment,Like,DisLike
from . permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self,serializer):
        """sets the authenticated user to the author of the post when creating """
        return serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly,)

class UserPostsListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(get_user_model(), id=user_id)
        return Post.objects.filter(author=user)

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        """return the coments for a particlar post"""
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id=post_id)
    
    def perform_create(self, serializer):
        """ associate the comment with a particular post and the author as the current user"""
        post_id = self.kwargs['post_id']
        post= get_object_or_404(Post,id=post_id)
        return serializer.save(author=self.request.user,post=post)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post__id = post_id)

class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    permission_classes =(permissions.IsAuthenticated,)
    serializer_class = LikeSerializer

    def perform_create(self,serializer):
        user = self.request.user
        post = self.get_post()
        existing_like = Like.objects.filter(user=user,post=post)

        if existing_like:
            existing_like.delete()
        else:
            serializer.save(user=user,post=post)
    
    def get_post(self):
        post_id = self.kwargs.get['post_id']
        return generics.get_object_or_404(Post,post_id)

class DislikeCreateView(generics.CreateAPIView):
    queryset = DisLike.objects.all()
    permission_classes =(permissions.IsAuthenticated,)
    serializer_class = DisLikeSerializer
    
    def perform_create(self,serializer):
        user = self.request.user
        post = self.get_post()
        exisiting_dislike = DisLike.objects.filter(user=user,post=post)

        if exisiting_dislike:
            exisiting_dislike.delete()
        else:
            serializer.save(user=user,post=post)


    def get_post(self):
        post_id = self.kwargs.get['post_id']
        return generics.get_object_or_404(Post,post_id)
    
class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)

class DislikeListView(generics.ListAPIView):
    serializer_class = DisLikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return DisLike.objects.filter(post_id=post_id)