from django.urls import path
# from accounts.views import UserRegistrationView, LoginAPIView, UserDetailView, UserEditView
from accounts.views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserDetailView.as_view(), name='detail'), #ユーザー情報取得
    path('profile/edit/', UserEditView.as_view(), name='update'),
    path('logout/', LogoutAPIView.as_view(),name='logout'), #ログアウト
]