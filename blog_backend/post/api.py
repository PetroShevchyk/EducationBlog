from django.shortcuts import render
from django.http import JsonResponse
from django.db import models
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, CategoriesSerializer
from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from .models import Post, Like, Comment, Categories
from .forms import PostForm, PostAttachmentForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from notification.utils import create_notification
from scripts.generate_categories import categories_update
# Create your views here.


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()

    user = User.objects.get(email=request.user)
    user = UserSerializer(user)

    category = request.GET.get('category', '')
    print(category)
    if category:
        posts = posts.filter(body__contains=category)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse({'data': serializer.data,
                         'user': user.data}, safe=False)


@api_view(['GET'])
def post_list_profile(request, id):
    posts = Post.objects.all()
    liked_posts = []
    for post in posts:
        likes = post.likes.all()
        for like in likes:
            if like.created_by.pk == id:
                liked_posts.append(post)
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_friendship_request = True

    if request.user in user.friends.all():
        can_send_friendship_request = False

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if check1 or check2:
        can_send_friendship_request = False

    return JsonResponse({'posts': post_serializer.data,
                         'user': user_serializer.data,
                         'liked_posts': PostSerializer(liked_posts, many=True).data,
                         'can_send_friendship_request': can_send_friendship_request}, safe=False)


@api_view(['GET'])
def liked_posts_list(request, id):
    posts = Post.objects.all()
    liked_posts = []
    for post in posts:
        likes = post.likes.all()
        for like in likes:
            if like.created_by.pk == id:
                liked_posts.append(post)
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)
    post_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({'posts': post_serializer.data,
                         'user': user_serializer.data,
                         'liked_posts': PostSerializer(liked_posts, many=True).data}, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachmentForm = PostAttachmentForm(request.POST, request.FILES)

    if attachmentForm.is_valid():
        attachment = attachmentForm.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user

        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        categories_update()
        
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})
    


@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, 'post_like', post_id=post.id)
    
        return JsonResponse({'message': 'like created'})
    else: 
        return JsonResponse({'message': 'post already liked'})
    

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return JsonResponse({
        'post': PostDetailSerializer(post).data,
    })


@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, 'post_comment', post_id=post.id)

    serializer = CommentSerializer(post)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def show_followings(request):
    user = User.objects.get(email=request.user)
    posts = Post.objects.all()
    friends = user.friends.all()
    following_posts = []
    for friend in friends:
        for post in posts:
            if friend.pk == post.created_by.pk:
                following_posts.append(post)
    user = UserSerializer(user)
    posts = PostSerializer(posts, many=True).data
    
    return JsonResponse({'following_posts': PostSerializer(following_posts, many=True).data}, safe=False)


@api_view(['GET'])
def get_categories(request):
    categories = Categories.objects.all()
    serializer = CategoriesSerializer(Categories.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({'message': 'post deleted'})