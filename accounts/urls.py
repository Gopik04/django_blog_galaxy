from django.urls import path
from.views import*

urlpatterns = [
    path('login/',user_login,name='login'),
    path('logout/',user_logout,name='logout'),
    path('register/',register_user,name='register'),
    path('profile/<str:username>/<str:id>',user_profile,name='profile'),
    path('update_profile/<str:username>/<str:id>',update_profile,name='update_profile'),
    
]