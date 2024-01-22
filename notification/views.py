from django.shortcuts import render
from rest_framework import generics,permissions
from .serializers import NotificationSerializer
from .models import Notification

# Create your views here.
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes =(permissions.IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user,is_read=False)
    