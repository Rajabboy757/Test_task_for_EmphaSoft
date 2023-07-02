from django.contrib import admin
from .models import Room, Brone


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'places', 'daily_price')
    ordering = ['id']
    list_display_links = ('id', 'number')
    search_fields = 'number',
    list_filter = ('places',)
    list_per_page = 50  # No of records per page


class BroneAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'broned_by', 'broned_from', 'broned_to')
    ordering = ['id']
    list_display_links = ('id', 'room')
    search_fields = 'room',
    list_filter = ('room', 'broned_by')
    list_per_page = 50  # No of records per page


admin.site.register(Room, RoomAdmin)
admin.site.register(Brone, BroneAdmin)

