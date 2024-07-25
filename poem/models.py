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