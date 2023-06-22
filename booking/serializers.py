from rest_framework import serializers
from accounts.serializers import User_public_serializer
from .models import Free_trial
from gym.models import Gym
from rest_framework.fields import empty

class Free_trial_serializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    gym=serializers.SerializerMethodField()
    class Meta:
        model = Free_trial
        fields = [
            'id',
            'booking_ID',
            'user',
            'gym',
            'type',
            'date',

        ]

    def get_user(self, obj):
        return User_public_serializer(obj.user).data
    def get_gym(self,obj):
        return obj.gym.gym_ID

    # def __init__(self,instance=None, data=empty, **kwargs):
    #     super().__init__(instance=instance, data=data, **kwargs)
    #     print(data)