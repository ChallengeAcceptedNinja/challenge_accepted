from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new$', views.InitiateChallenge.as_view(), name='new'),
    url(r'^(?P<challenge_id>\d+)$', views.JoinChallenge.as_view(), name='join')
]