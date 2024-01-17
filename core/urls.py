from django.urls import path
from . import views

urlpatterns=[

    path('register/',views.CreateUserView.as_view(),name='register'),
    path('token/',views.CreateUserTokenView.as_view(),name='user_token'),
    path('profile/',views.ManageUserView.as_view(),name='profile'),
    path('<int:user_id>/create_follow',views.FollowCreateView.as_view(),name='follow'),
]