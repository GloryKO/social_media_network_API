from django.db import models
from core.models import CustomUser
from django.contrib.auth import get_user_model
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author} - {self.text}'