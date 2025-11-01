from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'manager' and
            request.method in SAFE_METHODS + ('PUT', 'PATCH')
        )


class IsUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'user' and
            request.method in SAFE_METHODS
        )


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)
        if role == 'admin':
            return True
        elif role == 'manager':
            return request.method in SAFE_METHODS + ('PUT', 'PATCH')
        elif role == 'user':
            return request.method in SAFE_METHODS
        return False
