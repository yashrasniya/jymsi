from rest_framework import serializers
from accounts.serializers import User_public_serializer
from .models import Free_trial


class Free_trial_serializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

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
