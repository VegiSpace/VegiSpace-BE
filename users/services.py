import os
import string
import random
import datetime
from email.mime.image import MIMEImage
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_jwt.settings import api_settings

from users.models import UserData
from users.selectors import UserSelector

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserService:
    def __init__(self):
        pass
    
    def login(self, email:str, password: str):
        user_selector = UserSelector()

        user = user_selector.get_user_from_email(email)

        if not user_selector.check_password(user, password):
            raise exceptions.ValidationError(
                {'detail': "아이디나 비밀번호가 올바르지 않습니다."})
        
        token = RefreshToken.for_user(user=user)
        
        data={
            'email':user.email,
            'refresh': str(token),
            'access': str(token.access_token),
            'nickname': user.nickname
        }

        return data
    
    def logout(self, refresh: str):
        try:
            RefreshToken(refresh).blacklist()

        except TokenError:
            raise InvalidToken()