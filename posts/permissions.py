from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self,request,view):
        """checks if the suer is authenticated """
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permissions(self,request,view,obj):
        """read permisiions only alllowed for any request """
        if request.method in  permissions.SAFE_METHOD:
            return True
        return obj.author == request.user
    

        

