from rest_framework.permissions import BasePermission, IsAuthenticated

class IsStuff(BasePermission):
    message = "You are not allowed to access this resource."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
    

# он работает с объектом 
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
    
