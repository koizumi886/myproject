from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):
        # バリデーション
        if not username:
            raise ValueError('ユーザIDを入力してください')
        if not email:
            raise ValueError('メールアドレスを入力してください')
        if not password:
            raise ValueError('パスワードを入力してください')
        # Eメールを正規化
        email = self.normalize_email(email)
        # モデルインスタンス
        user = self.model(username=username, email=email, **extra_fields)
        # ハッシュ化
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # extra_fieldsは、ユーザーを作成する際に追加で設定できる属性の辞書
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
                raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    # ユーザーIDは英数字のみを許可するバリデータを設定
    # 英字（大文字・小文字）および数字のみで構成されているかをチェック
    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]*$',  # 英数字のみ
        message='ユーザーIDは英数字のみで構成してください。'
    )

    username = models.CharField(max_length=20, unique=True, validators=[username_validator], blank=False)
    email = models.EmailField(unique=True, blank=False)
    nickname = models.CharField(max_length=20, blank=False)
    comment = models.CharField(max_length=100, blank=True)

    # ログイン有無
    is_active = models.BooleanField(default=True)

    # 管理サイトへのアクセス権限
    is_staff = models.BooleanField(default=False)

    # ユーザー作成やスーパーユーザー作成などのカスタムロジック
    objects = UserManager()
    USERNAME_FIELD = 'username'
    # 管理コマンドを使用してスーパーユーザーを作成する際に必要とされるフィールド
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username