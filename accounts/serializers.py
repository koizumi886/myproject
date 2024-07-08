from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import re

# カスタムユーザーモデルを使用している場合は、
# 取得するユーザーモデルを指定する必要があります。
User = get_user_model()

#　新規登録用のシリアライザ
# ModelSerializerはDjangoモデルをJSONに変換したり、
# JSONをモデルに変換したりするためのロジックを持っています。
class  UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    # シリアライザをカスタマイズ
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm',)
        # パスワードを書き込み専用にしてレスポンスに含めない
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # シリアライザの値が有効かどうかを検証する
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': '確認パスワードと一致しません'})
        return attrs
    
    # usernameに英数字以外が含まれていないかを検証⇒Userでバージョン
    # def validate_username(self, value):
    #     if not re.match(r'^[a-zA-Z0-9]*$', value):
    #         raise serializers.ValidationError('ユーザーIDは英数字のみで入力してください')
    #     return value
    
    # ユーザーを作成
    def create(self, validated_data):
        # validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

#　ログインシリアライザ
class LoginSerializer(serializers.Serializer):
    # usernameとpasswordを受け取る
    username = serializers.CharField()
    # style={'input_type': 'password'}により、APIブラウザでパスワードフィールドがマスクされます。
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            #  Djangoの authenticate 関数を使用して、提供されたユーザーIDとパスワードで認証
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = '提供された認証情報ではログインできません'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'usernameとpasswordを入力してください'
            raise serializers.ValidationError(msg, code='authorization')

        # 認証が成功した場合、attrs 辞書に認証されたuser(必要な認証情報や追加の検証後のデータが含まれる)を追加
        attrs['user'] = user

        return attrs
    
# ユーザー情報取得のシリアライザ
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email','comment') 
        
# ユーザー情報編集のシリアライザ
class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'email','comment') 
        
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.email = validated_data.get('email', instance.email)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance