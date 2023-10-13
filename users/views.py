from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status

from .models import UserData, Profile
from users.services import UserService
from users.selectors import UserSelector

from .serializers import UserSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework.response import Response

# from rest_framework import serializers
# from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.pagination import PageNumberPagination

from users.mixins import ApiAuthMixin, ApiAllowAnyMixin

# view for registering users
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class UserListAPI(generics.ListAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserSerializer
    
    # def get(self, request):
    #     queryset = UserData.objects.all()
    #     serializer_class = UserSerializer
        # return Response(serializer_class.data)

class ProfileAPI(APIView):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs['user_email'])
        profile_serializer = ProfileSerializer(profile)
        return Response(profile_serializer.data)
    
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
#리팩토링 완료
class UserGetApi(APIView, ApiAuthMixin):
    class UserGetOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        nickname = serializers.CharField()
        email = serializers.EmailField()
        phone = serializers.CharField()
        data_joined = serializers.DateField()

    def get(self, request):
        selector = UserSelector()
        user = selector.get_user(user = request.user)
        serializer = self.UserGetOutputSerializer(user)

        return Response({
            'status': 'success',
            'data': serializer.data,
        }, status = status.HTTP_200_OK)
    
class UserLoginApi(APIView, ApiAllowAnyMixin):
    permission_classes = (AllowAny,)

    class UserLoginInputSerializer(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField()
    
    class UserLoginOutputSerializer(serializers.Serializer):
        email = serializers.CharField()
        refresh = serializers.CharField()
        access = serializers.CharField()
        nickname = serializers.CharField(allow_blank = True)

    def post(self, request):
        input_serializer = self.UserLoginInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        service = UserService()

        login_data = service.login(
            email=data.get('email'),
            password = data.get('password'),
        )

        output_serializer = self.UserLoginOutputSerializer(data = login_data)
        output_serializer.is_valid(raise_exception=True)

        return Response({
            'status':'success',
            'data':output_serializer.data,
        }, status=status.HTTP_200_OK)