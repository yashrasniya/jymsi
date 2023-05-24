from rest_framework import serializers
from gym.models import Gym, Facilities, Trainer, Reviews, Image, Timing,Deals

from accounts.serializers import User_public_serializer, User
from jymsi_backend.utilitys import image_add_db


class facilities_serializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = [
            'id',
            'Facilities_name',
            'icon',
        ]

class Deals_serializer(serializers.ModelSerializer):
    class Meta:
        model =Deals
        fields = [
            'id',
            'deal_name',
            'price',
            'discounted_price',
            'discount',
        ]


class trainer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = [
            'id',
            'trainer_name',
            'trainer_image',
            'trainer_description',
        ]

    def update(self, instance, validated_data):
        image_add_db({'trainer_image': instance.trainer_image}, validated_data)
        data = {'trainer_name': '', 'trainer_description': ''}
        for i in data:
            if validated_data.get(i):
                data[i] = validated_data.get(i)
        super(trainer_serializer, self).update(instance, data)


class timing_serializer(serializers.ModelSerializer):
    class Meta:
        model = Timing
        fields = [
            'type',
            'opening',
            'closing',
        ]


class reviews_serializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = [
            'id',
            'reviews_text',
            'user',
            'dateTime',
            'rating',
        ]

    def get_user(self, obj):
        return User_public_serializer(obj.user).data


class Image_serializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'image'
        ]

    def update(self, instance, validated_data):
        image_add_db({'image': instance.image}, validated_data)


class gym_serializer(serializers.ModelSerializer):
    gym_facilities = facilities_serializer(many=True)
    gym_trainer = trainer_serializer(many=True)
    gym_reviews = reviews_serializer(many=True)
    gym_images = Image_serializer(many=True)
    gym_timing=timing_serializer()
    gym_deals=Deals_serializer(many=True)

    class Meta:
        model = Gym
        fields = [
            'id',
            'gym_name',
            'gym_address',
            'gym_PinCode',
            'gym_city',
            'gym_state',
            'gym_images',
            'gym_description',
            'gym_link',
            'gym_facilities',
            'gym_trainer',
            'gym_reviews',
            'gym_timing',
            'gym_holiday',
            'gym_deals',
        ]

    def update(self, instance, validated_data):
        only_data = ['gym_name', 'gym_address', 'gym_description', 'gym_link']
        data = {}
        for i in only_data:
            if validated_data.get(i, ''):
                data[i] = validated_data.get(i)
        super().update(instance, data)
