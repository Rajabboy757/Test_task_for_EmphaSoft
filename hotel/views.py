from rest_framework.response import Response

from .models import Brone, Room
from rest_framework import viewsets, generics, status
from .serializers import RoomSerializer, BroneSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from django_filters import rest_framework as filters
from accounts.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_datetime


class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="daily_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="daily_price", lookup_expr='lte')

    class Meta:
        model = Room
        fields = ['places']


class RoomList(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter


def is_free_for_period(room, date_from, date_to):
    brones = Brone.objects.filter(room=room)
    if brones:
        for brone in brones:
            if brone.broned_from < date_from < brone.broned_to or brone.broned_to > date_to > brone.broned_from:
                return False
    return True


class FreeRoomsForPeriod(generics.GenericAPIView):
    serializer_class = RoomSerializer

    def post(self, request):
        date_from = parse_datetime(request.data.get('broned_from'))
        date_to = parse_datetime(request.data.get('broned_to'))

        rooms = Room.objects.all()
        free_rooms_ids = []

        for room in rooms:
            if is_free_for_period(room, date_from, date_to):
                free_rooms_ids.append(room.id)

        free_rooms_for_period = Room.objects.filter(id__in=free_rooms_ids).values()
        return Response(free_rooms_for_period)


class BroneViewSet(viewsets.ModelViewSet):
    queryset = Brone.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = BroneSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.data.get('room')
        date_from = parse_datetime(serializer.data.get('broned_from'))
        date_to = parse_datetime(serializer.data.get('broned_to'))

        if is_free_for_period(room, date_from, date_to):
            Brone.objects.create(room_id=room, broned_by=request.user, broned_from=date_from, broned_to=date_to)
            return Response({'message': "brone has created succesfully"}, status=status.HTTP_201_CREATED)
        return Response({'message': "this room is already broned for this period"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = Brone.objects.filter(broned_by=request.user)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
