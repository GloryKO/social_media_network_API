from django.shortcuts import render
from rest_framework import generics,permissions
from . serializers import PostSerializer
from . models import Post
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

class userPostsListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(get_user_model(), id=user_id)
        return Post.objects.filter(author=user)