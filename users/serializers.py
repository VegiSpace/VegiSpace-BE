from rest_framework import serializers
from .models import UserData, Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "nickname", "password", "phone", 'agree_terms', 'agree_personal','agree_sms','agree_email']

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       nickname=validated_data['nickname'],
                                       phone = validated_data['phone'],
                                       agree_terms = validated_data['agree_terms'],
                                       agree_personal = validated_data['agree_personal'],
                                       agree_sms = validated_data['agree_sms'],
                                       agree_email = validated_data['agree_email'],
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = "__all__"
        fields = ['user', 'contact_number', 'profile_pic', 'bio', 'created', 'updated']