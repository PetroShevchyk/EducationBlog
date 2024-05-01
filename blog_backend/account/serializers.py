from rest_framework.serializers import ModelSerializer

from .models import User, FriendshipRequest


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'friends', 'friends_count', 'posts_count', 'get_avatar', 'get_certificate', 'info')


class FriendshipRequestSerializer(ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by',)