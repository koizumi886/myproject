from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotFound

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    オブジェクトレベルの権限で、ユーザーが自分自身の情報のみ更新可能とする
    """
    # def has_permission(self, request, view) -> bool:
    #     print('has_permission', request.method.lower())
    #     if request.method.lower() == 'get':
    #         return True
    def has_object_permission(self, request, view, obj):
        print('has_object_permission start', request.method)
        # if request.method == 'PUT':
        #     return True
        # getでは書き込み権限はそのユーザー自身にのみ許可したい
        print('obj.owner', obj.owner, 'user',request.user, obj.owner == request.user)
        if obj.owner != request.user:
            raise PermissionDenied("You do not have permission to update this user's profile.")
        return True