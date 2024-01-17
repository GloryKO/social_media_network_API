from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView,ListCreateAPIView,ListAPIView
from . serializers import UserSerializer,AuthTokenSerializer,FollowSerializer
from rest_framework import permissions,authentication
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsOwnerOrReadOnly
#from drf_yasg.utils import swagger_auto_schema
from . models import Follow

class CreateUserView(CreateAPIView):
    serializer_class = UserSerializer

class CreateUserTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

class ManageUserView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes =(permissions.IsAuthenticated,IsOwnerOrReadOnly,)
    authentication_classes =[authentication.TokenAuthentication]

    def get_object(self):
        return self.request.user

class FollowCreateView(CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        follower = self.request.user
        following_id = self.kwargs['user_id']
        serializer.save(follower=follower,following_id=following_id)

class FollowerListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes= (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_user_model().objects.get(id=user_id)
        return user.followers.all()
   

