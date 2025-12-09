# club/admin.py
from django.contrib import admin
from .models import AcademicYear, Unit, Resource, Event, UserProfile

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year',)  # ONLY FIELD THAT EXISTS

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'year')
    list_filter = ('year',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'resource_type', 'uploaded_at')
    list_filter = ('resource_type', 'uploaded_at')
    search_fields = ('title',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'created_by')
    list_filter = ('event_date',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
