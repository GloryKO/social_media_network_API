from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from core.models import CustomUser
from .models import Post,Comment
from .serializers import PostSerializer
from django.contrib.auth import get_user_model

POSTS_URL = reverse('post-list')

class PublicPostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(name='testname',email='testuser@example.com', password='testpass')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
      

    def create_post(self,title,content,author):
            return Post.objects.create(title=title,content=content,author=self.user)

    def test_retrieve_posts(self):
        """test post retrieval """
        Post.objects.create(title='Test Post 1', content='Content 1', author=self.user)
        Post.objects.create(title='Test Post 2', content='Content 2', author=self.user)

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_unauthenticated_post_returns_error(self):
        """ test unathorized posts """
        payload={'title':'test post','content':'test content'}
        res=self.client.post(POSTS_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_403_FORBIDDEN)

    def test_view_user_post_unauthenticated(self):
            url = reverse('user-posts-list',kwargs={'user_id':self.user.id})
            res = self.client.get(url)
            self.assertEqual(res.status_code,status.HTTP_200_OK)
    

    def test_view_user_posts_nonexistent_user(self):
        url = reverse('user-posts-list', kwargs={'user_id': 999})  # 999 is assumed to be a nonexistent user ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_comments(self):
        url = reverse('comment-list', kwargs={'post_id': self.post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_unauthenticated(self):
        url = reverse('comment-list', kwargs={'post_id': self.post.id})
        data = {'text': 'New Comment'}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 0)

class PrivatePostApitest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(name='testname',email='test@example.com',password='testpass')
        self.client.force_authenticate(self.user)
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        
    def test_authenticated_user_post(self):
        """Test authenticated user post successful """
        payload={'title':'test title','content':'test content'}
        res = self.client.post(POSTS_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data['id'])
        self.assertEqual(post.title,res.data['title'])
        self.assertEqual(post.content,res.data['content'])

    def test_update_authenticated_post(self):
        post=Post.objects.create(title='Old Title', content='Old Content', author=self.user)
        payload ={'title': 'Updated Title', 'content': 'Updated Content'}
        url = reverse('post-detail',args=[post.id])
        res = self.client.put(url,payload)
        post.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_delete_post_authenticated(self):
        post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        url = reverse('post-detail', args=[post.id])   
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())
    
    def test_delete_post_unauthenticated(self):
        post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        url = reverse('post-detail', args=[post.id])

        self.client.force_authenticate(user=None)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    
        self.assertTrue(Post.objects.filter(id=post.id).exists())
    
    def test_create_comment_authenticated(self):
        url = reverse('comment-list', kwargs={'post_id': self.post.id})
        data = {'text': 'New Comment','author':self.user.id,'post':self.post.id}
        response = self.client.post(url, data)
     
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_update_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, text='Original Comment')
        url = reverse('comment-detail', kwargs={'post_id': self.post.id, 'comment_id': comment.id})
        data = {'text': 'Updated Comment','author':self.user.id,'post':self.post.id}
        response = self.client.put(url, data)
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(id=comment.id).text, 'Updated Comment')

    def test_delete_comment(self):
        comment = Comment.objects.create(post=self.post, author=self.user, text='To be deleted')
        url = reverse('comment-detail', kwargs={'post_id': self.post.id, 'comment_id': comment.id})
        response = self.client.delete(url)
       
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)