from django.urls import path
from django.conf import settings
from .views import RegisterView, ProfileAPI, UserListAPI, UserLoginApi, UserLogoutApi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    #path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', RegisterView.as_view(), name="sign_up"),
    path('login/', UserLoginApi.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',UserLogoutApi.as_view(), name='logout'),
    path('<user_email>/profile/', ProfileAPI.as_view()),
    path('list/', UserListAPI.as_view()),
]