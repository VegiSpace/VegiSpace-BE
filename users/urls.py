from django.urls import path
from .views import RegisterView, ProfileAPI, UserListAPI
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name="sign_up"),
    path('api/<user_email>/profile/', ProfileAPI.as_view()),
    path('api/list/', UserListAPI.as_view()),
]