from django.urls import path
from booking.api.api_view import Free_trial_view,Token_varify,all_booking,all_booking_user

urlpatterns = [
    path('booking/free_trial/', Free_trial_view.as_view()),
    path('booking/varify/<int:token>/<int:user_id>/', Token_varify.as_view()),
    path('booking/all/', all_booking.as_view()),
    path('booking/user/all/', all_booking_user.as_view()),

]