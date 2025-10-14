from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ['full_name']}),)
    readonly_fields = ('full_name',)

    list_display = ('username', 'full_name', 'email')
    list_display_links = ('username', 'email', 'full_name')


admin.site.register(CustomUser, CustomUserAdmin)
