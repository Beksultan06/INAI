from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Разрешаем читать всем, а изменять только админам
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем читать всем, а изменять только владельцу
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
