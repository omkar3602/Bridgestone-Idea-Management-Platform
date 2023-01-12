from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new_submission', views.new_submission, name='new_submission'),
    path('onhold', views.onhold, name='onhold'),
    path('accepted', views.accepted, name='accepted'),
    path('rejected', views.rejected, name='rejected'),
]