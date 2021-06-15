"""
rest_api app URL Configuration
"""
from django.urls import path, include
from rest_framework import routers
from .views import TripViewSet, StatusAPIView

app_name = "rest_api"


router = routers.DefaultRouter()
router.register('trip', TripViewSet, basename='trip')


urlpatterns = [
    path('status/', StatusAPIView.as_view(), name="status"),
    path('', include(router.urls), name="endpoint"),
]
