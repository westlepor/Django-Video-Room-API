from rest_framework import routers
from django.urls import path
from . import views
from django.conf.urls import include

router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'signin', views.SignInViewSet)
router.register(r'updateuser', views.UpdateUserViewSet)
router.register(r'deleteuser', views.DeleteUserViewSet)
router.register(r'createroom', views.RoomViewSet)

urlpatterns = [
  path('api/', include(router.urls)),
  path('api/user/<username>', views.GetUserWithNameView.as_view()),
  path('api/room/<guid>', views.GetRoomWithIDView.as_view()),
  path('api/room/changehost/<new_host_name>', views.ChangeHostView.as_view()),
  path('api/room/join/<guid>/<username>', views.JoinRoomView.as_view()),
  path('api/room/leave/<guid>/<username>', views.LeaveRoomView.as_view()),
  path('api/room/search/<username>', views.SearchRoomView.as_view()),
]