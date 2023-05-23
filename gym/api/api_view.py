from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Gym, Facilities, Image, Trainer
from ..serializers import gym_serializer, facilities_serializer, Image_serializer, trainer_serializer
from accounts.api.api_view import error
from accounts.authentication.CustomAuthentication import PartnerAuthentication


def partner_check(request):
    if not request.user.is_partner:
        return Response(error('you are not a partner so you can not access this api')), True
    if Gym.objects.filter(user=request.user):
        return Gym.objects.filter(user=request.user)[0], False
    else:
        return Response(error('you are not created a gym profile plz make it first')), True


class Gym_view(APIView):
    permission_classes = [AllowAny]

    def get(self, request, gym_id=None):
        if not gym_id:

            ser = gym_serializer(Gym.objects.all(), many=True)
        else:
            ser = gym_serializer(Gym.objects.filter(id=gym_id), many=True)
        return Response(ser.data)


class Gym_create(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # this api is only for creating gym profile
        if not request.user.is_partner:
            return Response(error('you are not a partner so you can not access this api'))
        if Gym.objects.filter(user=request.user):
            gym_obj = Gym.objects.filter(user=request.user)[0]
        else:
            gym_obj = Gym.objects.create(user=request.user)

        gym_serializer.update(gym_serializer(), gym_obj, request.data)

        return Response(gym_serializer(gym_obj).data)


class Gym_Image_add(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_partner:
            return Response(error('you are not a partner so you can not access this api'))
        if Gym.objects.filter(user=request.user):
            gym_obj = Gym.objects.filter(user=request.user)[0]
        else:
            return Response(error('you are not created a gym profile plz make it first'))
        print(len(gym_obj.gym_images.all()))
        if len(gym_obj.gym_images.all()) > 5:
            return Response(error("you can only add 5 images in gym"))

        img_obj = Image.objects.create()
        Image_serializer.update(Image_serializer(), img_obj, request.data)
        gym_obj.gym_images.add(img_obj)
        gym_obj.save()
        return Response(gym_serializer(gym_obj).data)


class Gym_Image_remove(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, image_id):
        gym_obj, boll = partner_check(request)
        if boll: return gym_obj

        img_obj = gym_obj.gym_images.all().filter(id=image_id)
        if not img_obj:
            return Response(error("img id not found in your gym profile"))

        print(img_obj)
        img_obj[0].delete()
        return Response(gym_serializer(gym_obj).data)


class facilities_view(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(facilities_serializer(Facilities.objects.all(), many=True).data)


class facilities_action(APIView):
    permission_classes = [IsAuthenticated]

    # authentication_classes = [PartnerAuthentication]

    def get(self, request, facility_id):
        gym_obj, boll = partner_check(request)
        if boll: return gym_obj

        if not request.GET.get('action', ""):
            return Response(error("action is missing"))
        else:
            action = request.GET.get('action', "")
        facility_obj = Facilities.objects.filter(id=facility_id)
        if facility_obj:
            facility_obj = facility_obj[0]
            if action == 'add':
                gym_obj.gym_facilities.add(facility_obj)
            elif action == 'remove':
                gym_obj.gym_facilities.remove(facility_obj)
            else:
                return Response(error('action must be add or remove'))
            return Response(gym_serializer(gym_obj).data)
        else:
            return Response(error('facility id not found'))


class Gym_trainer_action(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action, trainer_id=None):
        gym_obj, boll = partner_check(request)
        if boll: return gym_obj
        if not action in ['add', 'remove','update']:
            return Response(error('action must be add or remove'))
        if action == 'add':
            trainer_obj = Trainer.objects.create()
            trainer_serializer().update(trainer_obj, request.data)
            gym_obj.gym_trainer.add(trainer_obj)
        elif action == 'remove':
            tar_obj = gym_obj.gym_trainer.filter(id=trainer_id)
            if not tar_obj:
                return Response(error('id not found in you gym profile'))
            tar_obj[0].delete()
        elif action == 'update':
            tar_obj = gym_obj.gym_trainer.filter(id=trainer_id)
            if not tar_obj:
                return Response(error('id not found in you gym profile'))
            trainer_serializer().update(tar_obj[0], request.data)

        return Response(gym_serializer(gym_obj).data)
