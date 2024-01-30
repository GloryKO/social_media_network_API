
from rest_framework import generics,permissions
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from core.permissions import IsOwnerOrReadOnly

class ChatRoomListCreateView(generics.ListCreateAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ChatRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly,)
