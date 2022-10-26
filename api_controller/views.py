from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .util import is_auth, update_or_create_user_tokens
from requests import Request, post

import string
import random


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class JoinRoom(APIView):
    """
    View that allows the user to type in a code
    to enter a room.  
    """

    def post(self, request, format=None):
        """
        Returns a Response that contains a message and an appropriate status
        code depending on whether the user gave the correct room code to join a room. 
        """
        lookup_url_kwarg = "code"
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        code = request.data.get(lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session["room_code"] = code
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)

            return Response(
                {"Bad Request": "Invalid Room Code"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"Bad Request": "Invalid post data, Did not find code key."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GetRoom(APIView):
    """
    View that allows a user to retrieve room information.
    """

    serializer_class = RoomSerializer
    lookup_url_kwarg = "code"

    def get(self, request, format=None):
        """
        Returns a Response that contains the current created room information, given the request and
        format of the request. If failed, it returns a status code and an
        appropriate error message.
        """
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'Bad Request': 'Code parameter not found in request.'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView):
    """
    View that allows a user to create a room with an appropriate code. 
    """
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        """
        Returns a Response with a message and appropriate status code determining
        if the user created the room successfully or failed to create it. 
        """
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            else:
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()
            self.request.session["room_code"] = room.code

        return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)


class UserInRoom(APIView):
    """
    Gets the information of a room
    """

    def get(self, request, format=None):
        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    """
    Appropriately removes the information about a room from
    the users' current session.
    """

    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            # Removes the room from the User's current session!
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()

        return Response({'Message': 'User has left the room!'}, status=status.HTTP_200_OK)


class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    # Will update our room if the host wants to change certain settings
    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')
            # Retrieves the current room avaliable.
            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'msg': 'Room not found.'}, status=status.HTTP_404_NOT_FOUND)

            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({'msg': 'You are not the host of this room.'}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

        return Response({'Bad Request': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)


# Returns a randomly generated string that will be used when making
# requests to Spotify. This is to prevent CSRF Attacks.
def generate_random_state(str_size):
    state = ""
    for i in range(1, str_size):
        state += random.choice(string.ascii_letters)
    return state

# Spotify Authentication (Refer to diagram in Spotify for developers Docs)


class AuthURL(APIView):
    # Step 1 of Auth code Flow
    def get(self, request, format=None):
        state = generate_random_state(16)
        scopes = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'state': state,
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

# Step two of auth code flow.


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }, headers={
        'Authorization': 'Basic ' + CLIENT_ID + ':' + CLIENT_SECRET, # Any problem that occurs during auth, LOOK AT HEADERS!
        'Content-Type': 'application/x-www-form-urlencoded'
    }).json()

    # Get access token and refresh token
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    print(refresh_token)

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    # Redirects to homepage after steps 1 and 2 are completed.
    return redirect('frontend:home')


class isAuthenicated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_auth(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
