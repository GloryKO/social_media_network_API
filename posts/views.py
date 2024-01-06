from django.shortcuts import render
from rest_framework import generics,permissions
from . serializers import PostSerializer
from . models import Post
from . permissions import IsAuthorOrReadOnly


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

