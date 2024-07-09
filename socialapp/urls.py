from django.urls import path
from socialapp import views
# from socialapp.models import post

urlpatterns=[
        path('',views.index, name='index'),
        path('sign_up/',views.sign_up,name='sign_up'),
        path('sign_in/',views.sign_in,name='sign_in'),
        path('sign_out/',views.sign_out,name='sign_out'),
        path('profile_settings/',views.profile_settings,name='profile_settings'),
        path('add_post/',views.add_post,name='add_post'),
        path('like_post/<int:post_id>/',views.like_post,name='like_post'),

]
