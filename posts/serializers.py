from . models import Post,Comment,Like,DisLike
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields='__all__'
        read_only_fields=('created_at','author')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id','user','post','created_at')
        read_only_fields =('id', 'user', 'created_at')

class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ('id', 'user', 'post', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
