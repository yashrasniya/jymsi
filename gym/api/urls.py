from django.contrib import admin
from django.urls import path
from gym.api.api_view import (Gym_view, facilities_view,
                              Gym_create, Gym_Image_add,
                              facilities_action, Gym_Image_remove, Gym_trainer_action)

urlpatterns = [
    path('gym/', Gym_view.as_view()),
    path('gym/<int:gym_id>/', Gym_view.as_view()),
    path('gym/create/', Gym_create.as_view()),
    path('facilities/', facilities_view.as_view()),
    path('facilities/action/<int:facility_id>/', facilities_action.as_view()),
    path('gym/image/add/', Gym_Image_add.as_view()),
    path('gym/image/remove/<int:image_id>/', Gym_Image_remove.as_view()),
    path('gym/trainer/<str:action>/', Gym_trainer_action.as_view()),
    path('gym/trainer/<str:action>/<int:trainer_id>/', Gym_trainer_action.as_view()),

]
