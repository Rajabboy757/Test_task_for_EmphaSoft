from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'email_verified', 'type')
    ordering = ['id']
    list_display_links = ('id', 'username')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('email_verified', 'type')
    readonly_fields = ('email_verified', 'type', 'verification_code', 'photo',
                       'date_joined', 'last_login', 'is_staff', 'is_active', 'is_superuser')
    exclude = ('password', 'groups', 'user_permissions')
    list_per_page = 50  # No of records per page


admin.site.register(User, UserAdmin)
