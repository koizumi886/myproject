from django.db import models
from concurrency.fields import AutoIncVersionField  # 追加
from accounts.models import User

class Image(models.Model):
    CATEGORY = {
        "1": "風景",
        "2": "植物",
        "3": "動物・ペット",
    }
    # file_name = models.CharField(max_length=100, blank=False)
    subject = models.CharField(max_length=1, choices=CATEGORY, blank=True)
    image = models.ImageField(
        upload_to="uploads/%Y/%m/%d/",
        verbose_name="画像",
        blank=True,
        null=True
    )
    created_datetime = models.DateTimeField()
    updated_datetime =models.DateTimeField()
    # 更新するたびに自動でインクリメント. 更新時にはバージョンの値が更新条件に自動的付加
    version = AutoIncVersionField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "image"
        
class Poem(models.Model):
    FORM = {
        "1": "ノーマル",
        "2": "ポエム風",
    }
    FONT = {
        "1": "ゴシック",  # font-family: 'Noto Sans JP', sans-serif;
        "2": "明朝",  # font-family: 'Noto Serif JP', sans-serif;
        "3": "丸ゴシック",  # font-family: 'M PLUS Rounded 1c', sans-serif;
    }
    #  related_name=<model_name>_set (defalut)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    file_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    title = models.CharField(max_length=40, blank=True)
    caption = models.CharField(max_length=1000, blank=True)
    classification = models.CharField(max_length=1, choices=FORM, blank=True)
    font = models.CharField(max_length=1, choices=FONT, blank=True)
    parent_poem_id = models.ManyToManyField("self")
    """
    ManyToManyField が同じモデルを指している場合、以下のフィールドが生成されます：
    id: リレーションの主キー。
    from_<model>_id: モデルを指すインスタンス (つまりソースインスタンス) の id です。
    to_<model>_id: リレーションシップの対象となるインスタンス (つまり、ターゲットモデル・インスタンス) の id 。
    Model.m2mfield.through.objects.all()
    """
    created_datetime = models.DateTimeField()
    updated_datetime =models.DateTimeField()
    version = AutoIncVersionField()
    