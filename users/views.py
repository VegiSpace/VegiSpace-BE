from django.shortcuts import render
from rest_framework.views import APIView
from .models import UserData, Profile
from .serializers import UserSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


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