from django.urls import path
from .views import home, tts_generate

urlpatterns = [
    path("", home),
    path("api/tts/", tts_generate),
]
