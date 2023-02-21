from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new_submission', views.new_submission, name='new_submission'),
    path('edit_submission/<id>/', views.edit_submission, name='edit_submission'),
    path('delete_submission/', views.delete_submission, name='delete_submission'),
    path('submission/<id>/', views.individual_submission, name='individual_submission'),
    path('update_status/', views.update_status_view, name='update_status'),
    path('add_BU', views.add_BU, name='add_BU'),
    path('invite_IC', views.invite_IC, name='invite_IC'),
    path('adminuser', RedirectView.as_view(url=reverse_lazy('admin:index')), name='adminuser'),

]