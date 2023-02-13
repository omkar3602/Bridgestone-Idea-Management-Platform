from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('signup_ic/', views.signup_IC, name='signup_IC'),
    path('logout/', views.logout_user, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]