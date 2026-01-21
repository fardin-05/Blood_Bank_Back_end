from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow only owners of an object to edit or delete it.
    GET requests are allowed for everyone.
    """

    def has_object_permission(self, request, view, obj):
        #=====Everyone can read=========
        
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        #=====Only owner can modify/delete=====

        return request.user.is_authenticated and obj.id == request.user.id
