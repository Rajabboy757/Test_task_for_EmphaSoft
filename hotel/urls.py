from django.urls import path, include
from .views import BroneViewSet, RoomFilters
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'brone', BroneViewSet)

urlpatterns = [
    path('room_filter', RoomFilters.as_view(), name='free_rooms_list'),
    path('', include(router.urls)),
]
