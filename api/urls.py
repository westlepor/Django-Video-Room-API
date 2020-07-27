from rest_framework import routers
from django.urls import path
from . import views
from django.conf.urls import include

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'room', views.RoomViewSet)

urlpatterns = [
  path('api/', include(router.urls))
]