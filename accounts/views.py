from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer, LoginSerializer, UserSerializer, UserEditSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .permission import IsOwnerOrReadOnly
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

# 新規登録用のView
# 作成に特化したCreateAPIView
class UserRegistrationView(generics.CreateAPIView):
    
    permission_classes = [permissions.AllowAny]
    
    # シリアライザの指定
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        # 取得したデータをデシリアライズ
        serializer = self.get_serializer(data=request.data)
        # エラーの場合、HTTP 400 Bad Requestを返却
        if serializer.is_valid(raise_exception=True):
            user = serializer.save() # シリアライズ
            return Response({'user': UserRegistrationSerializer(user).data, # デシリアライズ
                             'message': 'ユーザー登録が完了しました!'},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ログイン用のView
class LoginAPIView(APIView):
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Djangoの login 関数で認証後データでログイン処理
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            # session保存
            # request.session['username'] = request.user.username
            # print(request.session['username'])
            return Response({'message': 'ログインが成功しました！',
                            'token': token.key,
                            'username': user.username},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ユーザー情報取得用のView
class UserDetailView(APIView):
    
    #　認証確認
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        print('request.auth:', request.auth)
        # ユーザー名が指定されていない場合は現在のユーザー名をセット
        # http://127.0.0.1:8000/accounts/profile/?username=user06
        username = request.GET.get(key='username', default=request.user.username)

        if username == request.user.username:
            user = request.user
        else:
            # 他のユーザーを取得
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({"message": "ユーザーが見つかりませんでした。"},
                                status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# ユーザー情報更新用のView
# フロントでPATCHメソッドを使って送信させる
class UserEditView(generics.RetrieveUpdateAPIView):
    
    # 読み取りは全ユーザーに許可する。
    permission_classes = [permissions.IsAuthenticated]
    # オブジェクトレベルの権限は例外的に除外
    # permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    lookup_field = 'username'

    def get_object(self):
        # self.request.userはこの時点でUser.idで最新取得済み
        print('get_object')

        # print('username_cash=', self.request.user.username, self.request.user.id, 'session=', self.request.session['username'])
        print('username_cash=', self.request.user.username, self.request.user.id)

        # obj = self.request.user
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.request.user.username}
        obj = generics.get_object_or_404(queryset, **filter_kwargs)

        # 通常は以下checkを行わないとpermissionエラーが発生しない
        # self.check_object_permissions(self.request, obj)
        print('get_object after',self.request.user)

        return obj

# update後、sessionのusernameを更新する

# 一覧取得
# class IndexView(generics.ListView):
#     model = Shop

# 詳細取得
# class DetailView(generics.DetailView):
#     model = Shop

#ログアウト用のAPIView  ※クライアントでWindowを閉じる時必須
class LogoutAPIView(APIView):
    # このビューがトークン認証を使用し、認証済みのユーザーのみアクセスできるようにします
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # トークン削除&ログアウト
        print('request.auth:', request.auth)
        request.auth.delete()
        logout(request)
        return Response({"message":"ログアウトしました"},status=status.HTTP_200_OK)

# User削除用のAPIView
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # TODO ここでログインユーザを削除しているため、ユーザを指定するように修正が必要　またはログアウトとセットで使用するか
        return self.request.user

    def delete(self, request, *args, **kwargs):
        # オブジェクトを取得して削除
        obj = self.get_object()
        obj.delete()

        # カスタムレスポンスを返す
        return Response({"message": "ユーザーを削除しました！"}, 
                        status=status.HTTP_204_NO_CONTENT)