from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Notification(models.Model):
    user =models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.message}"
    
    