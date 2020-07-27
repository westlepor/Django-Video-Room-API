from django.db import models

# Create your models here.
class Users(models.Model):
  user_id = models.AutoField(primary_key=True)
  username = models.TextField(unique=True, max_length=255)
  password = models.CharField(max_length=50)
  mobile_token = models.CharField(max_length=255, blank=True, null=True)

class Rooms(models.Model):
  room_id = models.AutoField(primary_key=True)
  roomname = models.TextField(unique=False)
  guid = models.TextField(max_length=255)
  host_user = models.ForeignKey(Users, related_name='room', on_delete=models.CASCADE)
  participants = models.ManyToManyField(Users, blank=True)
  capacity_limit = models.IntegerField(default=5, blank=False)