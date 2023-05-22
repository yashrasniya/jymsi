from rest_framework import serializers
from gym.models import Gym, Facilities, Trainer, Reviews, Image
import random
import binascii
import base64
from django.core.files.base import ContentFile


class facilities_serializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = [
            'id',
            'Facilities_name',
            'icon',
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


class reviews_serializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = [
            'id',
            'reviews_text',
            'user',
            'dateTime',
            'rating',
        ]


class Image_serializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'id',
            'image'
        ]
    def update(self, instance, validated_data):
        file_array = {'image': instance.image}
        for i in file_array:
            print(validated_data.get(i, ''))
            if validated_data.get(i, ''):

                image_data = validated_data.get(i)
                # image_data = image_data.split("'")[1].split(';base64,')[1]
                try:
                    data = ContentFile(base64.b64decode(image_data))
                except binascii.Error as e:
                    print(e)
                    raise binascii.Error(f'{i} send data is in incorrect format it should be in bash 64')
                file_name = str(random.random()) + '.' + 'png'
                file_array[i].save(file_name, data, save=True)
                print('done')

class gym_serializer(serializers.ModelSerializer):
    gym_facilities = facilities_serializer(many=True)
    gym_trainer = trainer_serializer(many=True)
    gym_reviews = reviews_serializer(many=True)
    gym_images=Image_serializer(many=True)

    class Meta:
        model = Gym
        fields = [
            'id',
            'gym_name',
            'gym_address',
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
        only_data=['gym_name','gym_address','gym_description','gym_link']
        data={}
        for i in only_data:
            if validated_data.get(i,''):
                data[i]=validated_data.get(i)
        super().update(instance,data)