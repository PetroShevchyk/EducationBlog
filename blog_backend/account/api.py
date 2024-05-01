from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm, ProfileForm
from post.models import Post
from post.serializers import PostSerializer
from .models import FriendshipRequest, User
from .serializers import UserSerializer, FriendshipRequestSerializer
from notification.utils import create_notification



@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar(),
        'info': request.user.info,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    message = 'success'

    print(request.POST)
    print(request.FILES)
    form = SignupForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()

        # Send verification email later!
    else:
        message = 'error'

    return JsonResponse({'message': message})


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests,
    }, safe=False)


@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        friend_request = FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        notification = create_notification(request, 'new_friendrequest', friendrequest_id=friend_request.id)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})
    

@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    notification = create_notification(request, 'accepted_friendrequest', friendrequest_id=friendship_request.id)

    return JsonResponse({'message': 'friendship request updated'})


@api_view(['POST'])
def edit_profile(request):
    user = request.user
    email = request.data.get('email')
    print(request.data.get('info'))
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)

        return JsonResponse({'message': 'information updated', 'user': serializer.data})
    

@api_view(['GET'])
def show_certificate(request, pk):
    user = User.objects.get(id=pk)
    user = UserSerializer(user)

    return JsonResponse(user.data, safe=False)
