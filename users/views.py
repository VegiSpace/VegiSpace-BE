from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework import status

from .models import UserData, Profile
from users.services import UserService
# , UserPasswordService
from users.selectors import UserSelector

from .serializers import UserSerializer, ProfileSerializer
from rest_framework import generics
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# from drf_yasg.generators import SwaggerGenerator


# from rest_framework import serializers
# from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.pagination import PageNumberPagination

from users.mixins import ApiAuthMixin, ApiAllowAnyMixin

# view for registering users
class RegisterView(APIView):
    @swagger_auto_schema(
            request_body=UserSerializer,
            operation_summary='''회원가입''',
            operation_description='''email, password, name, phone 입력시 회원가입 ''',
            responses={
                "200": openapi.Response(
                    description="OK",
                    examples={
                        "application/json":{
                            "status":'success'
                        }
                    }
                ),
                "400": openapi.Response(
                    description="Bad Request",
                ),
            },
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class UserListAPI(APIView):
    permission_classes = (AllowAny,)

    class UserListOutputSerializer(serializers.Serializer):
        nickname = serializers.CharField()
        email = serializers.EmailField()
        phone = serializers.CharField()
        date_joined = serializers.DateTimeField()

    @swagger_auto_schema(
            operation_summary='전체 유저 리스트 조회',
            operation_description='''
                전체 유저의 리스트를 조회 합니다.
            ''',
            responses={
                "200":openapi.Response(
                    description="OK",
                    examples={
                        "application/json":{
                            'nickname':'vegispace',
                            'email':'vegispace@gmail.com',
                            'phone':'01012345678',
                            'date_joined':'2023-10-14',
                        },
                    }
                ),
                "400":openapi.Response(
                    description="Bad Request",
                ),
            },
    )
    def get(self, request):
        users = UserSelector.get_user_list(self)
        serializers=self.UserListOutputSerializer(users, many=True)

        return Response({
            'status':'success',
            'data': serializers.data,
        }, status=status.HTTP_200_OK)

    

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
    
    @swagger_auto_schema(
            request_body=UserLoginInputSerializer,
            operation_summary='''로그인''',
            operation_description='''email, password 입력시 로그인''',
            responses={
                "200": openapi.Response(
                    description="OK",
                    examples={
                        "application/json":{
                            'email':'vegispace@gmail.com',
                            'refresh':'refresh token',
                            'access':'access token',
                            'nickname':'vegispace'
                        }
                    }
                ),
                "400": openapi.Response(
                    description="Bad Request",
                ),
            },
    )
    
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
    
class UserLogoutApi(APIView, ApiAuthMixin):
    class UserLogoutSerializer(serializers.Serializer):
        refresh = serializers.CharField(required=True)

    @swagger_auto_schema(
            request_body=UserLogoutSerializer,
            operation_summary='''로그아웃''',
            operation_description='''refresh 토큰 입력시 로그아웃''',
            responses={
                "200": openapi.Response(
                    description="OK",
                    examples={
                        "application/json":{
                            "status":'success'
                        }
                    }
                ),
                "400": openapi.Response(
                    description="Bad Request",
                ),
            },
    )
    def post(self, request):
        serializer = self.UserLogoutSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = UserService()

        service.logout(
            refresh=data.get('refresh')
        )

        return Response({
            'status': 'success',
        }, status=status.HTTP_200_OK)
    
# class UserEmailCheckApi(APIView):
#     permission_classes = (AllowAny,)

#     class EmailCheckSerializer(serializers.Serializer):
#         email = serializers.EmailField()

#     @swagger_auto_schema(
#             request_body=EmailCheckSerializer,
#             operation_summary='''이메일 체크''',
#             operation_description='''email 필드 입력시 해당 이메일이 DB에 존재하는지 확인''',
#             responses={
#                 "200": openapi.Response(
#                     description="OK",
#                     examples={
#                         "application/json":{
#                             "status":'success'
#                         }
#                     }
#                 ),
#                 "400": openapi.Response(
#                     description="Bad Request",
#                 ),
#             },
#     )

#     def post(self, request):
#         serializer = self.EmailCheckSerializer(data=request.data)
#         serializer.is_valid()
#         data = serializer.validated_data

#         service = UserService()

#         check_email_message = service.check_email(
#             email = data.get('email')
#         )

#         return Response({
#             'status': 'success',
#             'data': check_email_message,
#         },status = status.HTTP_200_OK)
    
# class UserPasswordResetSendEmailApi(APIView):
#     permission_classes = (AllowAny, )

#     class PasswordEmailSerializer(serializers.Serializer):
#         email = serializers.EmailField()

#     @swagger_auto_schema(
#             request_body=PasswordEmailSerializer,
#             operation_summary='''비밀번호 재설정 이메일 발송''',
#             operation_description='''email 필드 입력시 비밀전호 재설정 이메일이 발송.''',
#             responses={
#                 "200": openapi.Response(
#                     description="OK",
#                     examples={
#                         "application/json":{
#                             "status":'success'
#                         }
#                     }
#                 ),
#                 "400": openapi.Response(
#                     description="Bad Request",
#                 ),
#             },
#     )

#     def post(self, request):
#         serializer = self.PasswordEmailSerializer(data=request.data)
#         serializer.is_valid()
#         data = serializer.validated_data

#         service = UserPasswordService()
#         service.password_reset_send_email(email = data.get('email'))

#         return Response({
#             'status': 'success',
#         }, status=status.HTTP_200_OK)