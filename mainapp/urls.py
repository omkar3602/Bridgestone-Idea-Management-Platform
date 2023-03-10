from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('new_submission/', views.new_submission, name='new_submission'),
    path('edit_submission/<key>/', views.edit_submission, name='edit_submission'),
    path('delete_submission/', views.delete_submission, name='delete_submission'),
    path('submission/<key>/', views.individual_submission, name='individual_submission'),
    path('update_status/', views.update_status_view, name='update_status'),
    path('add_BU/', views.add_BU, name='add_BU'),
    path('edit_BU/', views.edit_BU, name='edit_BU'),
    path('edit_BU/<id>/', views.edit_BU_single, name='edit_BU_single'),
    path('invite_IC/', views.invite_IC, name='invite_IC'),
    path('adminuser/', RedirectView.as_view(url=reverse_lazy('admin:index')), name='adminuser'),
    path('onhold/', views.on_hold, name='on_hold'),
    path('accepted/', views.accepted, name='accepted'),
    path('rejected/', views.rejected, name='rejected'),
    path('review_pending/', views.review_pending, name='review_pending'),


]