from django.shortcuts import render

from rest_framework import viewsets
# Create your views here.

from tracker.serializers import EventSerializer
from tracker.models import Event

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
