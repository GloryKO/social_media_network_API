
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self,request,view):
        if request.user.is_authenticated:
            return True
        return False
    
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHOD:
            return True
        return obj == request.user