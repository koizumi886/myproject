import os
from rest_framework import generics, permissions
from accounts.models import User
from backend.settings import MEDIA_ROOT
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer

class ImageViewSet(viewsets.ModelViewSet):
      #　認証確認
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
	      # 画像登録処理
       subject = request.data['subject']
       
       created_datetime = request.data['created_datetime']
       updated_datetime = request.data['updated_datetime']
       img_data = request.data['imageData']
       if img_data is not None:
            user = User.objects.get(username="user01")
            print(user.username)
           
            img = Image.objects.create(
                subject=subject,
                image=img_data,
                created_datetime=created_datetime,
                updated_datetime=updated_datetime,
                owner=user)
            return Response({'id': img.id, 'url': img.image.url},
                            status=status.HTTP_201_CREATED)
       return Response("Failed to register image.",
                        status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        print('instance.image.name ', instance.image.name)
        os.remove(str(MEDIA_ROOT) + '/' + instance.image.name)