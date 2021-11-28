from __future__ import unicode_literals
from rest_framework import routers
from django.conf.urls import include
from django.conf.urls import url
from django.urls import path
from .login import LoginAuthToken, check_token, ProfileViewSet
from .register import RegisterViewSet

router = routers.DefaultRouter()

app_name = 'api'

router.register(r'register', RegisterViewSet, basename="register")
router.register(r'profile', ProfileViewSet, basename="profile")

urlpatterns = [
    path('login', LoginAuthToken.as_view()),
    path('check-token/<str:token>', check_token, name="check-token"),
    url(r'^', include(router.urls)),
]

