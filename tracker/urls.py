from django.conf.urls import url
from django.contrib import admin

from rest_framework.routers import DefaultRouter


from tracker import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)


urlpatterns = router.urls
