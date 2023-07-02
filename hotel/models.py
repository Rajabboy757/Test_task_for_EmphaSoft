from django.db import models
from accounts.models import User


class Room(models.Model):
    number = models.CharField(max_length=4)
    daily_price = models.DecimalField(max_digits=6, decimal_places=2)
    places = models.IntegerField()

    def __str__(self):
        return self.number


class Brone(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    broned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    broned_from = models.DateTimeField()
    broned_to = models.DateTimeField()

