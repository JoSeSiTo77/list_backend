from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from backend_project.settings import SIMPLE_JWT

from .serializers import UserSerializer, MyTokenObtainPairSerializer

User = get_user_model()

# JWT Settings
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh_token = request.COOKIES.get(SIMPLE_JWT['NAME_COOKIE_REFRESH'])
        refresh_token_name = SIMPLE_JWT['NAME_COOKIE_REFRESH']

        refresh_lifetime = SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        response.set_cookie(
            key=refresh_token_name,
            value=response.data['refresh'],
            max_age=int(refresh_lifetime.total_seconds()),
            secure= SIMPLE_JWT['COOKIE_SECURE_PROTOCOLE'],
            httponly=True,
            samesite=SIMPLE_JWT['REFRESH_TOKEN_SAMESITE'],
        )

        del response.data['refresh']

        return response

class MyTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(SIMPLE_JWT['NAME_COOKIE_REFRESH'])
        refresh_token_name = SIMPLE_JWT['NAME_COOKIE_REFRESH']
        if refresh_token:
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                refresh_lifetime = SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

                response.set_cookie(
                    key=refresh_token_name,
                    value=response.data['refresh'],
                    max_age=int(refresh_lifetime.total_seconds()),
                    secure= SIMPLE_JWT['COOKIE_SECURE_PROTOCOLE'],
                    httponly=True,
                    samesite=SIMPLE_JWT['REFRESH_TOKEN_SAMESITE'],
                )
                del response.data['refresh']
                return response
        return Response({
            'detail': 'Refresh token not found'
            }, status=status.HTTP_401_UNAUTHORIZED)

class MyTokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(SIMPLE_JWT['NAME_COOKIE_REFRESH'])
        
        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            response.delete_cookie(SIMPLE_JWT['NAME_COOKIE_REFRESH'])

        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    user = request.user
    user = get_object_or_404(User, id=user.id)
    serializer = UserSerializer(user)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    refresh = RefreshToken.for_user(user)

    response = Response({
        'access': str(refresh.access_token),
        'user': serializer.data['first_name']
    }, status=status.HTTP_201_CREATED)

    refresh_lifetime = SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        max_age=int(refresh_lifetime.total_seconds()),
        secure= SIMPLE_JWT['COOKIE_SECURE_PROTOCOLE'],
        httponly=True,
        samesite=SIMPLE_JWT['REFRESH_TOKEN_SAMESITE'],
    )

    return response



@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manage_user(request):
    user = request.user
    user = get_object_or_404(User, id=user.id)
    if request.method == 'PUT':
        user = get_object_or_404(User, id=user.id)
        print(user)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'User successfully updated',
            'new_data': serializer.data
        }, status=status.HTTP_200_OK)
    if request.method == 'DELETE':
        user = get_object_or_404(User, id=user.id)
        user.delete()

        return Response({
            'message': 'User successfully deleted'
        }, status=status.HTTP_200_OK)

