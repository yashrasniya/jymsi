from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'name',
            'email',
            'mob_number'
        ]

    def update(self, instance, validated_data):
        read_only=['id','mob_number']
        validated_data._mutable=True
        for i in read_only:
            if validated_data.get(i,''):
                validated_data.pop(i)
        super().update(instance,validated_data)

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'mob_number'
        ]