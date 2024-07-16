from django.contrib import admin
from .models import Profile, Unit


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date')  # Adjust based on the fields you want to display
    search_fields = ('user__username', 'birth_date')  # Fields to search in the admin interface


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Adjust based on the fields you want to display
    search_fields = ('name', 'description')  # Fields to search in the admin interface


admin.site.register(Profile)
admin.site.register(Unit)
