from django.urls import path
from .views import SubscribeView

urlspattern = [
    path('subscribe', SubscribeView.as_view(), name='subscribe'),
]