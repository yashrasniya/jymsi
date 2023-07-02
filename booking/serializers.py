from rest_framework import serializers
from accounts.serializers import User_public_serializer
from .models import Free_trial
from gym.models import Gym
from rest_framework.fields import empty
from gym.serializers import gym_serializer
import datetime

class Free_trial_serializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    gym=serializers.SerializerMethodField()
    verified=serializers.SerializerMethodField()
    class Meta:
        model = Free_trial
        fields = [
            'id',
            'booking_ID',
            'user',
            'gym',
            'type',
            'date',
            'verified',
            'cancel',

        ]

    def get_user(self, obj):
        return User_public_serializer(obj.user).data
    def get_gym(self,obj):
        return obj.gym.gym_ID
    def get_verified(self,obj):
        is_valid = obj.date - datetime.date.today()
        print(is_valid.days, obj.date, datetime.date.today())
        if not obj.valid:
            return True
        if is_valid.days >= 0:
            return False
        return 'Expired'



class Free_trial_serializers_user(Free_trial_serializers):
    def __init__(self,instance=None, data=empty, **kwargs):
        super(Free_trial_serializers, self).__init__(instance=instance, data=data, **kwargs)
        self.Meta.fields.append('token')
    def get_gym(self,obj):
        return gym_serializer(obj.gym).data
