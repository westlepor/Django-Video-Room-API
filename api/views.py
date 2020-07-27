import bcrypt
import jwt
import hashlib
import uuid

from django.shortcuts import render
from django.core import serializers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users, Rooms
from .serializers import UserSerializer, RoomSerializer

from room.settings import SECRET_KEY

class UserViewSet(viewsets.ModelViewSet):
  lookup_field='user_id'
  queryset = Users.objects.all()
  serializer_class = UserSerializer

class SignInViewSet(viewsets.ModelViewSet):
  lookup_field='user_id'
  queryset = Users.objects.all()
  serializer_class = UserSerializer
  def create(self, request):    
    try:
      username = request.data['username']
      password = request.data['password']
      user = Users.objects.get(username=username)
      if user.password == password:
        token = jwt.encode({'user_id': user.user_id}, SECRET_KEY, algorithm='HS256').decode('UTF-8')
        return Response({
          'success':True,
          'token':token
        })
      else:
        return Response({
          'success':True,
          'token':None
        })
    except Exception as e:
      print(e)
      return Response({
        'success':False,
        'token':None
      })

class UpdateUserViewSet(viewsets.ModelViewSet):
  lookup_field='user_id'
  queryset = Users.objects.all()
  serializer_class = UserSerializer
  def create(self, request):
    try:
      if request.META['HTTP_AUTHORIZATION'][:6] != 'Bearer':
        return Response({
          'success':False,
        })
      token = request.META['HTTP_AUTHORIZATION'][7:]
      decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256')
      user = Users.objects.get(user_id=decoded['user_id'])
      for data in request.data:
        if data == 'password':
          user.password = request.data['password']
        elif data == 'mobile_token':
          user.mobile_token = request.data['mobile_token']
      user.save()
      return Response({
        'success':True
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False
      })

class DeleteUserViewSet(viewsets.ModelViewSet):
  lookup_field='user_id'
  queryset = Users.objects.all()
  serializer_class = UserSerializer
  def list(self, request):
    try:
      if request.META['HTTP_AUTHORIZATION'][:6] != 'Bearer':
        return Response({
          'success':False,
        })
      token = request.META['HTTP_AUTHORIZATION'][7:]
      decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256')
      user = Users.objects.get(user_id=decoded['user_id'])
      user.delete()
      return Response({
        'success':True
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False
      })

class GetUserWithNameView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      username = self.kwargs['username']
      user = Users.objects.get(username=username)
      return Response({
        'success':True,
        'user':serializers.serialize('json', [user])
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False,
        'user': None
      })

class RoomViewSet(viewsets.ModelViewSet):
  lookup_field='room_id'
  queryset = Rooms.objects.all()
  serializer_class = RoomSerializer
  def create(self, request):
    try:
      if request.META['HTTP_AUTHORIZATION'][:6] != 'Bearer':
        return Response({
          'success':False,
        })
      token = request.META['HTTP_AUTHORIZATION'][7:]
      decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256')
      user = Users.objects.get(user_id=decoded['user_id'])
      roomname = request.data['roomname']
      room = Rooms.create(roomname, user)
      room.save()
      token = jwt.encode({'user_id': decoded['user_id'], 'guid':str(room.guid)}, SECRET_KEY, algorithm='HS256').decode('UTF-8')
      return Response({
        'success':True,
        'token':token
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False,
        'token':None
      })

class JoinRoomView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      if request.META['HTTP_AUTHORIZATION'][:6] != 'Bearer':
        return Response({
          'success':False,
        })
      room = Rooms.objects.get(guid=uuid.UUID(self.kwargs['guid']))
      user = Users.objects.get(username=self.kwargs['username'])
      room.participants.add(user)
      return Response({
        'success':True
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False
      })

class LeaveRoomView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      if request.META['HTTP_AUTHORIZATION'][:6] != 'Bearer':
        return Response({
          'success':False,
        })
      room = Rooms.objects.get(guid=uuid.UUID(self.kwargs['guid']))
      user = Users.objects.get(username=self.kwargs['username'])
      room.participants.remove(user)
      return Response({
        'success':True
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False
      })

class ChangeHostView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      if request.META['HTTP_AUTHORIZATION'][:6] != 'Bearer':
        return Response({
          'success':False,
        })      
      token = request.META['HTTP_AUTHORIZATION'][7:]
      decoded = jwt.decode(token, SECRET_KEY, algorithms='HS256')
      user = Users.objects.get(user_id=decoded['user_id'])
      room = Rooms.objects.get(guid=uuid.UUID(decoded['guid']))
      new_host_user = Users.objects.get(username=self.kwargs['new_host_name'])
      if room.host_user == user:
        room.host_user = new_host_user
        room.save()
        return Response({
          'success':True
        })
      else:
        return Response({
          'success':False
        })
    except Exception as e:
      print(e)
      return Response({
        'success':False
      })

class GetRoomWithIDView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      guid = self.kwargs['guid']
      room = Rooms.objects.get(guid=uuid.UUID(guid))
      return Response({
        'success':True,
        'room':serializers.serialize('json', [room])
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False,
        'room': None
      })

class SearchRoomView(APIView):
  def get(self, request, *args, **kwargs):
    try:
      username = self.kwargs['username']
      rooms = Rooms.objects.all()
      room_list = []
      for room in rooms:
        if room.host_user.username == username:
          room_list.append(room.roomname)
          break
        for particiipant in room.participants.all():
          if particiipant == username:
            room_list.append(room.roomname)
      return Response({
        'success':True,
        'room_list':room_list
      })
    except Exception as e:
      print(e)
      return Response({
        'success':False,
        'room_list': None
      })