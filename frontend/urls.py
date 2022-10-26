from .views import index
from django.urls import path

app_name = 'frontend'

# URL patterns for the user.
urlpatterns = [
    path('', index, name='home'),
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index)
]