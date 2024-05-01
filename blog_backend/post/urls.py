from django.urls import path, include
from . import api


urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('create/', api.post_create, name='post_create'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('following/', api.show_followings, name='show_followings'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('liked_posts/<uuid:id>/', api.liked_posts_list, name='liked_posts'),
    path('categories/', api.get_categories, name='categories'),
    path('<uuid:pk>/delete/', api.post_delete, name='post_delete'),
]
