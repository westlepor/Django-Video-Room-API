import uuid
from django.db import models

# Create your models here.
class Users(models.Model):
  user_id = models.AutoField(primary_key=True)
  username = models.CharField(unique=True, max_length=20, blank=False)
  password = models.CharField(max_length=50, blank=False)
  mobile_token = models.CharField(max_length=255, blank=True, null=True)

class Rooms(models.Model):
  guid = models.UUIDField(default=uuid.uuid4,
        editable=False, unique=True, db_index=True)
  roomname = models.CharField(blank=True, max_length=20)
  host_user = models.ForeignKey(Users, related_name='room', on_delete=models.CASCADE, blank=False)
  participants = models.ManyToManyField(Users, blank=True)
  capacity_limit = models.IntegerField(default=5, blank=True)

  @classmethod
  def create(cls, roomname, host_user):
    room = cls(roomname=roomname, host_user=host_user)
    return room