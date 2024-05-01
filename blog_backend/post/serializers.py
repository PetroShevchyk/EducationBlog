from .models import Post, PostAttachment, Comment, Categories
from rest_framework.serializers import ModelSerializer

from account.serializers import UserSerializer



class PostAttachmentSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = PostAttachment
        fields = ('id', 'created_by','get_image',)


class PostSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments_count', 'created_by', 'created_at_formatted', 'attachments')


class CommentSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)


class PostDetailSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'created_by', 'created_at_formatted', 'comments', 'attachments',)


class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'hashtag', 'occurences',)
