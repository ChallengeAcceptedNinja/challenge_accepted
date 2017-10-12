from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new$', views.InitiateChallenge.as_view(), name='new'),
    url(r'^join$', views.JoinChallenge.as_view(), name='join'),
]