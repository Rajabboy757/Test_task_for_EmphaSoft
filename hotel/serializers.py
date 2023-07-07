from rest_framework import serializers
from .models import Room, Brone


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'daily_price', 'places')


class BroneSerializer(serializers.ModelSerializer):
    room = RoomSerializer()

    class Meta:
        model = Brone
        fields = ('id', 'room', 'broned_by', 'broned_from', 'broned_to')