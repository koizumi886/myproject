import os
from rest_framework import generics, permissions
from accounts.models import User
from backend.settings import MEDIA_ROOT
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Image
from .serializers import *
from accounts.permission import IsOwnerOrReadOnly
from rest_framework.views import APIView
from accounts.serializers import *
import json, uuid


# イメージAPI
class ImageViewSet(viewsets.ModelViewSet):
      #　認証確認
    permission_classes = [permissions.IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

	# 画像登録処理
    def create(self, request, *args, **kwargs):
       subject = request.data['subject']
       created_datetime = request.data['created_datetime']
       updated_datetime = request.data['updated_datetime']
       img_data = request.data['imageData']
       if img_data is not None:
            print(request.user.id, request.user.username)
            user = User.objects.get(id=request.user.id)
           
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
        
class PoemSetList(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        
        """
        Return a list of all users.
        """
        # poems = Poem.objects.select_related('file_id').all()
        data = [{'imageId':Poem.objects.get(file_id=poems.file_id).file_id.id,
                     'url':Poem.objects.get(file_id=poems.file_id).file_id.image.url,
                     'title':poems.title,
                     'caption':poems.caption,
                     'owner':poems.owner,
                     'nickname':poems.owner.nickname,
                     } for poems in Poem.objects.select_related('file_id').all()]
        poemSetSerializer = PoemSetSerializer(data=data, many=True)
        poemSetSerializer.is_valid()
        # for poem in poems:
        #     title = poem.title
        #     data = {
        #         'title' : title,
        #         # 'image' : request.data['img_imageData'],
        #         # 'created_datetime' : request.data['img_created_datetime'],
        #         # 'updated_datetime': request.data['img_updated_datetime'],
        #         # 'owner' : 2
        #         }
        # serializer1 = PoemSetListSerializer(data=data)

        print('list',poemSetSerializer.data)
        return Response(poemSetSerializer.data, status=status.HTTP_200_OK)

# セット登録のView
class ImagePoemAPIView(APIView):

    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly]
    
    # def get(self, request, format=None):
    #     """
    #     Return a list of all users.
    #     """
    #     # images = [{'image_id':image.id, 'url':image.image} for image in Image.objects.all()]
    #     # poem = [{'poem_id':poem.id, 'titile':poem.title, 'caption':poem.caption} for poem in Poem.objects.all()]
    #     images = [image.image for image in Image.objects.all()]
    #     # poem = [{poem.id, poem.title, poem.caption} for poem in Poem.objects.all()]
    #     poem = Poem.objects.all()
    #     return Response(
    #         {poem},
    #                 status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        print('my_param', pk)
        # クエリパラメータの場合
        # imageId = self.request.query_params.get(key='image')
        image = Image.objects.get(id=pk)
        image.delete()
        # poem = Poem.objects.get(file_id=imageId)
        # poem.objects.delete()
        return Response({"message": "投稿を削除しました！"}, 
                status=status.HTTP_200_OK)
    
    def post(self, request):
        data = {
            'subject' : request.data['img_subject'],
            'image' : request.data['img_imageData'],
            'created_datetime' : request.data['img_created_datetime'],
            'updated_datetime': request.data['img_updated_datetime'],
            'owner' : request.user.id
            }
        serializer1 = ImageSerializer(data=data)
        
        if serializer1.is_valid(raise_exception=True):
            print("is_valid 3")
            image = serializer1.save() # create
            serializer1 = ImageSerializer(image)
            print('serializer1',serializer1)
            imageId = serializer1.data['id'], # シリアライズ
            imageUrl = serializer1.data['image'],
            
        data2 = {
            'file_id' : image.id,
            'title' : request.data['title'],
            'caption' : request.data['caption'],
            'classification' : request.data['classification'],
            'font' : request.data['font'],
            'created_datetime' : request.data['img_created_datetime'],
            'updated_datetime': request.data['img_updated_datetime'],
            'owner' : request.user.id
            }
        serializer2 = PoemSerializer(data=data2)
        if serializer2.is_valid(raise_exception=True):
            poem = serializer2.save() # create
            serializer2 = PoemSerializer(poem)
            poemId = serializer2.data['id'], # シリアライズ
            return Response(
                {
                'image_id': imageId,
                'image_url': imageUrl,
                'poem_id': poemId},
                        status=status.HTTP_200_OK)

# キャプションAPI
class PoemViewSet(viewsets.ModelViewSet):
    http_method_names = [
        "get",
        # "post",
        # "put",
        # "patch",
        # "delete",
        "head",
        "options",
        "trace",
    ]
    #　認証確認
    permission_classes = [permissions.IsAuthenticatedOrReadOnly & IsOwnerOrReadOnly]
    queryset = Poem.objects.all()
    serializer_class = PoemSerializer

    def create(self, request, *args, **kwargs):
        # 登録処理
       file_id = request.data['file_id']
       title = request.data['title']
       caption = request.data['caption']
       classification = request.data['classification']
       font = request.data['font']
    #    parent_poem_id = request.data['parent_poem_id']
       created_datetime = request.data['created_datetime']
       updated_datetime = request.data['updated_datetime']
       
       if file_id is not None:
            user = User.objects.get(id=request.user.id)
            image = Image.objects.get(id=file_id)
            # parent_poem = Poem.objects.get(id=1)
           
            poem = Poem.objects.create(
                file_id=image,
                title=title,
                caption=caption,
                classification=classification,
                font=font,
                created_datetime=created_datetime,
                updated_datetime=updated_datetime,
                owner=user)
            # poem.save()
            # poem.parent_poem_id.add(parent_poem)
            return Response({'id': poem.id, 'title': poem.title},
                            status=status.HTTP_201_CREATED)
            
       return Response("Failed to register poem.",
                        status=status.HTTP_400_BAD_REQUEST)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
        print('deleted the poem ')