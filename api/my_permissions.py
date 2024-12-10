from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Разрешить доступ только администраторам для всех действий
            return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # Разрешить доступ только администраторам для изменения объекта
            return request.user and request.user.is_staff

class IsSupplierOrConsumer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user and (request.user.user_type == 'supplier' or request.user.user_type == 'consumer')

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if view.action in ['partial_update']:
                return True
            return False

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # Разрешить доступ на изменение только владельцу объекта
            return obj == request.user

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user and (request.user.is_staff or request.user == obj)

class IsSupplierOrConsumerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            if user.is_staff or user.user_type in ['consumer', 'supplier']:
                return True

