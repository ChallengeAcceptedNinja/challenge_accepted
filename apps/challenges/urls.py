from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup$', views.ChallengeView.as_view(), name='signup'),
]