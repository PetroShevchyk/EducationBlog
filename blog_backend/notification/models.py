from django.db import models
import uuid

from account.models import User
from post.models import Post


class Notification(models.Model):
    FRIENDREQUEST = 'new_friendrequest'
    POST_LIKE = 'post_like'
    POST_COMMENT = 'post_comment'
    ACCEPTEDFRIENDREQUEST = 'accepted_friendrequest'
    REJECTEDFRIENDREQUEST = 'rejected_friendrequest'

    CHOICES_TYPE_OF_NOTIFICATION = (
        (FRIENDREQUEST, 'New friend request'),
        (ACCEPTEDFRIENDREQUEST, 'Accepted friend request'),
        (REJECTEDFRIENDREQUEST, 'Rejected friend request'),
        (POST_COMMENT, 'Post comment'),
        (POST_LIKE, 'Post like')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_notification', on_delete=models.CASCADE)
    created_for = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
