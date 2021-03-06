from django.urls import path, include
from .views import GetRoom, RoomView, CreateRoomView, JoinRoom

# URL patterns to access the api.
urlpatterns = [
    path('', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('get-room', GetRoom.as_view()),
    path('join-room', JoinRoom.as_view())
]