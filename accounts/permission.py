from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotFound

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    オブジェクトレベルの権限で、ユーザーが自分自身の情報のみ更新できるようにする。
    読み取りは全ユーザーに許可する。
    """
    # def has_permission(self, request, view) -> bool:
    #     print('has_permission', request.method.lower())
    #     if request.method.lower() == 'get':
    #         return True
    def has_object_permission(self, request, view, obj):
        print('has_object_permission start', request.method)
        raise PermissionDenied("You do not have permission to update this user's profile.")
        if request.method == 'PUT':
            return True
        # getでは書き込み権限はそのユーザー自身にのみ許可したい
        # request.user.username(変更前)と比較する
        # return obj.username == request.session['username']
        print('has_object_permission', obj.username, request.user.username, obj.username == request.user.username)
        if obj.username != request.user.username:
            print('false')
            raise PermissionDenied("You do not have permission to update this user's profile.")
        return obj.username == request.user.username