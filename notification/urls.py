from django.urls import path
from .views import *
urlpatterns = [
 path('', NotificationListView.as_view(), name='notification-list'),
 path('notifications/mark-read/<int:pk>/', MarkNotificationsReadView.as_view(), name='mark-notification-read'),

]
