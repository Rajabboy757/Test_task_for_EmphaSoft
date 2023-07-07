from django.urls import path, include
from .views import BroneViewSet, FreeRoomsForPeriod
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'brone', BroneViewSet)

urlpatterns = [
    path('free_rooms_for_period/', FreeRoomsForPeriod.as_view(), name='free_rooms_list'),
    path('', include(router.urls)),
]
