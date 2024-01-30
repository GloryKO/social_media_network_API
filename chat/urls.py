# chat/urls.py
from django.urls import path
from .views import ChatRoomListCreateView, ChatRoomDetailView, MessageListCreateView, MessageDetailView

urlpatterns = [
    path('chat-rooms/', ChatRoomListCreateView.as_view(), name='chat-room-list'),
    path('chat-rooms/<int:pk>/', ChatRoomDetailView.as_view(), name='chat-room-detail'),
    path('messages/', MessageListCreateView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]
