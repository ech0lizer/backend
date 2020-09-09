from django.urls import path
from .views import RegisterAPIView, EmailVerifyAPIView, LoginAPIView, UserInfoAPIView, UserLogoutAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify-email/', EmailVerifyAPIView.as_view(), name='verify-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('user/', UserInfoAPIView.as_view(), name='user'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
]
