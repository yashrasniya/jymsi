from rest_framework import serializers
from gym.models import Gym, Facilities, Trainer, Reviews, Image, Timing, Deals
from rest_framework.fields import empty
from accounts.serializers import User_public_serializer, User
from jymsi_backend.utilitys import image_add_db
from booking.models import Free_trial
from django.contrib.auth.models import AnonymousUser


def partner_check(request):
    if not request.user.is_partner:
        return
    if Gym.objects.filter(user=request.user):
        return Gym.objects.filter(user=request.user)[0], False
    else:
        return

class facilities_serializer(serializers.ModelSerializer):
    added=serializers.SerializerMethodField()
    class Meta:
        model = Facilities
        fields = [
            'id',
            'Facilities_name',
            'icon',
            'added',
        ]
    def get_added(self,obj):
        if self.context.get('user','') and not type(self.context.get('user')) == AnonymousUser:
            user=self.context.get('user')
            print(user)
            if not user.is_partner:
                return False
            if Gym.objects.filter(user=user):
                return True if obj in  Gym.objects.get(user=user).gym_facilities.all() else False
            else:
                return False
        else:
            return False

class Deals_serializer(serializers.ModelSerializer):
    class Meta:
        model = Deals
        fields = [
            'id',
            'months',
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
            'id',
            'type',
            'opening',
            'closing',
        ]


class reviews_serializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    permission =serializers.SerializerMethodField()

    class Meta:
        model = Reviews
        fields = [
            'id',
            'reviews_text',
            'user',
            'dateTime',
            'rating',
            'permission',
        ]

    def get_user(self, obj):
        return User_public_serializer(obj.user).data
    def get_permission(self,obj):
        if self.context.get('user',''):
            return True if obj.user==self.context.get('user') else False
        return False


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
    gym_facilities = serializers.SerializerMethodField()
    gym_trainer = trainer_serializer(many=True)
    gym_reviews = serializers.SerializerMethodField()
    gym_images = Image_serializer(many=True)
    gym_timing = timing_serializer(many=True)
    gym_deals = Deals_serializer(many=True)
    review_count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    gym_rating = serializers.SerializerMethodField()
    booked = serializers.SerializerMethodField()

    class Meta:
        model = Gym
        fields = [
            'id',
            'gym_ID',
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
            'gym_rating',
            'price',
            'review_count',
            'gym_timing',
            'gym_holiday',
            'gym_deals',
            'booked',
        ]

    def update(self, instance, validated_data):
        only_data = ['gym_name', 'gym_address', 'gym_description', 'gym_link',
                     'gym_city', 'gym_state', 'gym_PinCode']
        data = {}
        for i in only_data:
            if validated_data.get(i, ''):
                data[i] = validated_data.get(i)
        super().update(instance, data)
    def get_gym_facilities(self,obj):
        return facilities_serializer(obj.gym_facilities,many=True,context=self.context).data
    def get_review_count(self, obj):
        return len(obj.gym_reviews.all())

    def get_price(self, obj):
        data = {'per_month': 10000000000000, 'deals': ''}

        for i in obj.gym_deals.all():
            try:
                m = int(i.months)
                if data['per_month'] > int(i.discounted_price) / m:
                    data['deals']=i
                    data['per_month'] = round(int(i.discounted_price) / m)
                    # data['per_month'] = int(i.discounted_price) / m
            except Exception as e:
                pass
        if data['per_month'] == 10000000000000:
            return 0
        data['deals'] = Deals_serializer(data['deals']).data

        return data
    def get_gym_rating(self,obj):
        round=0
        for i in obj.gym_reviews.all():
            try:
                round+=int(i.rating)
            except ValueError as e:
                print(e)
        if obj.gym_reviews.all():
            return round/len(obj.gym_reviews.all())
        return 0
    def get_booked(self,obj):
        if self.context.get('user','') and not type(self.context.get('user')) == AnonymousUser:
            user=self.context.get('user')
            if Free_trial.objects.filter(user=user,gym=obj,valid=True,cancel=False):
                return True
            if Free_trial.objects.filter(user=user, gym=obj, valid=False, cancel=False):
                return 'Verified'
        return False
    def get_gym_reviews(self,obj):
        return reviews_serializer(obj.gym_reviews,many=True,context=self.context).data

class my_gym(gym_serializer):
    def __init__(self,instance=None, data=empty, **kwargs):
        super(my_gym, self).__init__(instance=instance, data=data, **kwargs)
        self.Meta.fields.append('gym_mobile_number')
        self.Meta.fields.append('gym_landLine_number')
        self.Meta.fields.append('visible')