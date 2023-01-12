from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new_submission', views.new_submission, name='new_submission')
]