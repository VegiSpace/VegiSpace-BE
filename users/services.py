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
        
#     def check_email(self, email: str):
#         user_selector = UserSelector()

#         check_email = user_selector.check_email(email)

#         if(check_email):
#             return '존재하는 이메일입니다.'
        
#         return '존재하지 않는 이메일입니다. '
    
# class UserPasswordService:
#     def __init__(self):
#         pass

#     #인증번호 생성 함수
#     def email_auto_string():
#         LENGTH = 5
#         string_pool = string.ascii_letters + string.digits
#         auth_string=""
#         for i in range(LENGTH):
#             auth_string += random.choice(string_pool)
#         return auth_string

#     def password_reset_send_email(self, email:str):
#         user_selector = UserSelector()

#         user = user_selector.get_user_from_email(email)

#         payload = JWT_PAYLOAD_HANDLER(user)
#         jwt_token = JWT_ENCODE_HANDLER(payload)
#         code = UserPasswordService.email_auto_string()

#         html_content = render_to_string('password_reset.html',{
#             'user': user,
#             'nickname': user.nickname,
#             'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
#             'token': jwt_token,
#             'code': code,
#         })


#         user.code = code
#         user.save()

#         mail_subject = '[VegiSpace] 비밀번호 변경 메일입니다.'
#         to_email = user.email
#         from_email = 'vegispace@gmail.com'
#         msg = EmailMultiAlternatives(
#             mail_subject,'...',from_email,[to_email])
#         msg.attach_alternative(html_content, "text/html")
#         # file_path = os.path.join(
#         #     settings.BASE_DIR, 'static/img/LOGO.png')
#         # img_data = open(file_path, 'rb').read()
#         # image = MIMEImage(img_data)
#         # image.add_header('Content-ID', '<{}>'.format('LOGO.png'))
#         # msg.attach(image)

#         msg.send()

