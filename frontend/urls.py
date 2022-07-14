from .views import index
from django.urls import path

# URL patterns for the user.
urlpatterns = [
    path('', index),
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index)
]