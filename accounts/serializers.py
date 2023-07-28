from rest_framework import serializers
from accounts.models import User
from jymsi_backend.utilitys import image_add_db


class UserSerializer(serializers.ModelSerializer):
    profile_img=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'user_ID',
            'name',
            'first_name',
            'last_name',
            'email',
            'mob_number',
            'profile_img',
            'is_partner',
        ]
    def get_profile_img(self,obj):
        if obj.profile_img:
            if 'https' in str(obj.profile_img.url):
                return str(obj.profile_img)
            else:
                return str(obj.profile_img.url)


class User_public_serializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name',            'user_ID',

            'profile_img',
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'user_ID',

            'name',
            'first_name',
            'last_name',
            'email',
            'mob_number',
            'profile_img',
            'is_partner'
        ]

    def update(self, instance, validated_data):
        read_only = ['id','user_ID', 'mob_number', 'name', 'profile_img']
        image_add_db({'profile_img': instance.profile_img}, validated_data,instance=instance)
        # validated_data._mutable=True
        for i in read_only:
            if validated_data.get(i, ''):
                validated_data.pop(i)
        print(type(validated_data))
        super().update(instance, validated_data)

