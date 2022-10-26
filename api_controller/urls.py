from django.urls import path, include
from .views import GetRoom, RoomView, CreateRoomView, JoinRoom, UserInRoom, LeaveRoom, UpdateRoom, AuthURL, spotify_callback, isAuthenicated

# URL patterns to access the api.
urlpatterns = [
    path('', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('get-room', GetRoom.as_view()),
    path('join-room', JoinRoom.as_view()),
    path('user-in-room', UserInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),
    path('update-room', UpdateRoom.as_view()),


    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenicated', isAuthenicated.as_view())
]
