from django.db import models
from core.models import CustomUser

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    