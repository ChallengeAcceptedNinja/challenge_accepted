from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new$', views.InitiateChallenge.as_view(), name='new'),
    url(r'^(?P<challenge_id>\d+)$', views.JoinChallenge.as_view(), name='join'),
    url(r'^bouts$', views.Bouts.as_view(), name='bouts'),
    url(r'^(?P<bout_id>)$', views.DetermineResult.as_view(), name='determine')
]