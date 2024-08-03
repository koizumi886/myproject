from rest_framework import serializers
from .models import *

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"

class PoemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poem
        fields = "__all__"
        read_only_fields = ['parent_poem_id']

class PoemSetListSerializer(serializers.ListSerializer):
    # child = PostSerializer()
    def create(self, validated_data):
        return validated_data

class PoemSetSerializer(serializers.Serializer):
    imageId = serializers.IntegerField()
    url = serializers.CharField()
    title = serializers.CharField()
    caption = serializers.CharField()
    owner = serializers.CharField()
    nickname = serializers.CharField()
    class Meta:
        list_serializer_class = PoemSetListSerializer

class  ImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = "__all__"
    
    # ユーザーを作成
    def create(self, validated_data):
        # validated_data.pop('password_confirm')
        # reqUser = self.context.get('user')
        # userObj = User.objects.get(id=reqUser.id)
        print("create 4")
        # userObj = User.objects.get(id=2)
        print("validated_data",validated_data)

        image = Image.objects.create(**validated_data
            # subject = self.data.subject,
            # image = validated_data['imageData'],
            # created_datetime = validated_data['img_created_datetime'],
            # updated_datetime = validated_data['img_updated_datetime'],
            # owner = userObj
        )
        return image
    
class  PoemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poem
        # fields = "__all__"
        exclude = ['parent_poem_id']
    
    # ユーザーを作成
    def create(self, validated_data):
        # reqUser = self.context.get('user')
        # userObj = User.objects.get(id=reqUser.id)
        # userObj = User.objects.get(id=2)
        # image = Image.objects.get(id=validated_data['file_id'])
        poem = Poem.objects.create(**validated_data
            # file_id = image,
            # title = validated_data['title'],
            # caption = validated_data['caption'],
            # classification = validated_data['classification'],
            # font = validated_data['font'],
            # created_datetime = validated_data['created_datetime'],
            # updated_datetime = validated_data['updated_datetime'],
            # owner = userObj
        )
        return poem