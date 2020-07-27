from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users, Rooms
from .serializers import UserSerializer, RoomSerializer

class UserViewSet(viewsets.ModelViewSet):
  lookup_field='user_id'
  queryset = Users.objects.all()
  serializer_class = UserSerializer

class RoomViewSet(viewsets.ModelViewSet):
  lookup_field='room_id'
  queryset = Rooms.objects.all()
  serializer_class = RoomSerializer