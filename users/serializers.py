from rest_framework import serializers
from .models import UserData, Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password", "phone"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name'],
                                       phone = validated_data['phone']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # fields = "__all__"
        fields = ['user', 'contact_number', 'profile_pic', 'bio', 'created', 'updated']