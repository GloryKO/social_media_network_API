from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from core.models import CustomUser
from .models import Post
from .serializers import PostSerializer
from django.contrib.auth import get_user_model

POSTS_URL = reverse('post-list')

class PublicPostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(name='testname',email='testuser@example.com', password='testpass')

    def test_retrieve_posts(self):
        Post.objects.create(title='Test Post 1', content='Content 1', author=self.user)
        Post.objects.create(title='Test Post 2', content='Content 2', author=self.user)

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)