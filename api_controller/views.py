from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room

# Create your views here.


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