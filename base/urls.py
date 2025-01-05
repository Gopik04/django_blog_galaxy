from django.urls import path
from.views import*

urlpatterns = [
    path('home/',home,name='home' ),
    path('read_post/<str:id>/<str:slug>',read_post,name='read_post' ),
    path('posts/<str:category>/',post_category,name='post_category' ),
]