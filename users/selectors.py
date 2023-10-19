from typing import List
from django.http import Http404, HttpResponseBadRequest
from django.db.models import QuerySet, Q, F
#from django.contrib.auth import authenticate

from users.models import UserData

class UserSelector:
    def __init__(self):
        pass

    def get_user(user):
        user_id = user.id
        return UserData.objects.get(id =user_id)
    
    def get_user_list(self):
        data = UserData.objects.all()
        print(data)
        return data

    #이메일에 해당하는 유저 객체 리턴 함수
    @staticmethod
    def get_user_from_email(email:str) ->UserData:
        try:
            return UserData.objects.get(email=email)
        except UserData.DoesNotExist:
            raise Http404
        except UserData.MultipleObjectsReturned:
            raise Http404
        
    #주어진 비밀번호가 User객체의 비밀번호와 일치하는지 여부 리턴
    @staticmethod
    def check_password(user: UserData, password:str):
        return user.check_password(password)
    
    #주어진 이메일을 가진 사용자 객체가 존재하는지 여부 리턴
    @staticmethod
    def check_email(email: str):
        return UserData.object.filter(email=email).exist()
    
    #주어진 닉네임을 가진 사용자 객체가 존재하는지 여부 리턴
    @staticmethod
    def check_name(nickname: str):
        return UserData.objects.filter(nickname=nickname).exists()
    