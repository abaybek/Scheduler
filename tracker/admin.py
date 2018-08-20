from django.contrib import admin

# Register your models here.
from tracker.models import Event
from tracker.forms import EventAdminForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start', 'end')
    list_filter = ('start', )
    
    form = EventAdminForm