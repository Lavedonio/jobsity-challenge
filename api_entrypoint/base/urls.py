"""
base app URL Configuration
"""
from django.urls import path
from .views import HomePageView

app_name = "base"

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
]
