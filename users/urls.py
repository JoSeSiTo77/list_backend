from django.urls import path
from .views import register, get_users, manage_user
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from users.views import MyTokenObtainPairView, MyTokenBlacklistView, MyTokenRefreshView


urlpatterns = [
    path('api/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('api/logout/', MyTokenBlacklistView.as_view(), name='logout'),
    path('api/refresh/', MyTokenRefreshView.as_view(), name='refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='verify'),
    path('register/', register, name='register'),
    path('user/', get_users, name='showone'),
    path('manage/', manage_user, name='manage'),
]