from rest_framework import serializers
from .models import Users, Rooms

class UserSerializer(serializers.ModelSerializer):
  user_id = serializers.ReadOnlyField()
  class Meta:
    model = Users
    fields = [
      'user_id',
      'username',
      'password',
      'mobile_token'
    ]

class RoomSerializer(serializers.ModelSerializer):
  room_id = serializers.ReadOnlyField()
  class Meta:
    model = Rooms
    fields = [
      'roomname',
      'guid',
      'host_user',
      'participants',
      'capacity_limit'
    ]