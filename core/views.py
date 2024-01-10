from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from . serializers import UserSerializer,AuthTokenSerializer
from rest_framework import permissions,authentication
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsOwnerOrReadOnly
#from drf_yasg.utils import swagger_auto_schema

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
    