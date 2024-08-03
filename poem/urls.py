from django.urls import path, include
from rest_framework.routers import DefaultRouter
from poem.views import *
from django.conf.urls.static import static
from django.conf import settings

# ImageViewSetを設定
router = DefaultRouter()
router.register(r'image', ImageViewSet, basename="image")
router.register(r'caption', PoemViewSet, basename="caption")

urlpatterns = [
    path('', include(router.urls)),
    path('poemSet/', ImagePoemAPIView.as_view(), name='poemSet'),
    path('poemSet/<int:pk>/', ImagePoemAPIView.as_view()),
    path('poemSet/list/', PoemSetList.as_view()),
    # path('delete/', ImagePoemAPIView.as_view(), name='register'),
]
