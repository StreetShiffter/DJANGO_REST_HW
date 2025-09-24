from rest_framework import permissions


# class IsModerator(permissions.BasePermission):
#     """Только модераторы могут читать и редактировать — но не создавать и не удалять."""
#     def has_permission(self, request, view):
#         if request.method in ['GET', 'PUT', 'PATCH']:
#             return request.user.groups.filter(name='Moderator').exists()
#         return False  # POST и DELETE — запрещены модераторам
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['GET', 'PUT', 'PATCH']:
#             return request.user.groups.filter(name='Moderator').exists()
#         return False
#
#
# class IsOwner(permissions.BasePermission):
#     """Только владелец может делать всё: создавать, читать, редактировать, удалять."""
#     def has_permission(self, request, view):
#         if request.method == 'POST':
#             return request.user.is_authenticated
#         return True
#
#     def has_object_permission(self, request, view, obj):
#         return obj.owner == request.user


class IsOwnerOrModerator(permissions.BasePermission):
    """Объединение: владелец — всё, модератор — только чтение и редактирование, никто другой — ничего."""
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and not request.user.groups.filter(name='Moderator').exists()
        if request.method in ['GET']:
            return request.user.is_authenticated
        return True  # PUT/PATCH/DELETE — проверяются в has_object_permission

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:  # Админ — бог!
            return True
        if obj.owner == request.user:
            return True
        if request.user.groups.filter(name='Moderator').exists():
            return request.method in ['GET', 'PUT', 'PATCH']  # DELETE — запрещён!
        return False