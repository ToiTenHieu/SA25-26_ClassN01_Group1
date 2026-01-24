from django.urls import path
from . import views
app_name = 'account'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('regis_by_fb/', views.regis_by_fb, name='regis_by_fb'),
    path('regis_by_gg/', views.regis_by_gg, name='regis_by_gg'),
       
]