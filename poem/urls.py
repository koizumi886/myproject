from django.urls import path, include
from rest_framework.routers import DefaultRouter
from poem.views import ImageViewSet
from django.conf.urls.static import static
from django.conf import settings

# ImageViewSetを設定
router = DefaultRouter()
router.register(r'image', ImageViewSet, basename="image")

urlpatterns = [
    path('', include(router.urls)),
]
