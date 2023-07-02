from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from gym.models import Gym
from accounts.api.api_view import error
from ..serializers import Free_trial_serializers,Free_trial_serializers_user
from ..models import Free_trial
from gym.serializers import gym_serializer
import random
from gym.api.api_view import partner_check
from accounts.models import User
import datetime
from django.shortcuts import redirect



class Free_trial_view(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.GET.get('gym', ''):
            return Response(error("gym id not found"))
        gym_obj = Gym.objects.filter(gym_ID=request.GET.get('gym'))
        if not gym_obj:
            return Response(error("gym id not found"))

        n = True
        while n:
            ID = random.randint(10000, 99999)
            if not Free_trial.objects.filter(booking_ID=f"B{ID}"):
                n = False
        ser = Free_trial_serializers(data=request.GET)
        gym_ID=Gym.objects.filter(gym_ID=request.GET['gym'])[0]
        if ser.is_valid():
            if Free_trial.objects.filter(gym=gym_obj[0], user=request.user):
                return Response(error('you all ready claim the trial!'))
            obj = ser.save(user=request.user, booking_ID=f"B{ID}",gym=gym_ID)
            obj.token = random.randint(1000, 9999)
            obj.gym = Gym.objects.filter(gym_ID=request.GET['gym'])[0]
            obj.save()
            return Response({'data': ser.data, 'token': obj.token})
        else:
            return Response(error('', error=ser.errors))


class Token_varify(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token, user_id):
        gym_obj, boll = partner_check(request)
        if boll: return gym_obj
        user_obj = User.objects.filter(id=user_id)
        if not user_obj:
            return Response(error('user id not found'))
        trial_obj = Free_trial.objects.filter(token=token, user=user_obj[0], valid=True)
        if not trial_obj:
            return Response(error("code not found in this user"))
        is_valid = trial_obj[0].date - datetime.date.today()
        print(is_valid.days, trial_obj[0].date, datetime.date.today())
        if is_valid.days == 0:
            trial_obj[0].valid = False
            trial_obj[0].save()
            return Response(Free_trial_serializers(trial_obj[0]).data)
        elif is_valid.days > 0:
            return Response(error('you are too early '))
        else:
            return Response(error('you are too late!'))

class Free_trial_action(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,action,trail_id):
        if not action in ['cancel', 'edit']:
            return Response(error('action must be cancel or edit'))
        obj=Free_trial.objects.filter(booking_ID=trail_id)
        if not obj:
            return Response(error('trail id not found'))
        if not obj[0].valid:
            return Response(error('trail id is verified so You can not cancel it!'))
        if request.user!=obj[0].user:
            return Response(error('trail id is not related to you!'))
        if action=='cancel':
            obj[0].cancel=True
        if action=='edit':
            if request.GET.get('gym',''):
                return Response(error('you can not add gym id only booking id! '))
            ser_obj=Free_trial_serializers(obj[0],data=request.GET)
            if not ser_obj.is_valid():
                return Response(error('', error=ser_obj.errors))
            obj=ser_obj.save()

        return all_booking_user().get(request)



class all_booking(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gym_obj, boll = partner_check(request)
        if boll: return gym_obj
        return Response(Free_trial_serializers(
            Free_trial.objects.filter(gym=gym_obj), many=True,context={'user':request.user}).data)

class all_booking_user(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(Free_trial_serializers_user(
            Free_trial.objects.filter(user=request.user), many=True,context={'user':request.user}).data)


