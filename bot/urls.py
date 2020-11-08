from django.urls import path
from .views import *

urlpatterns = [
    path('', messenger_download_bot),
]
