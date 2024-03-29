from django.urls import path
from . import views

urlpatterns=[

    path('register/',views.CreateUserView.as_view(),name='register'),
    path('token/',views.CreateUserTokenView.as_view(),name='user_token'),
    path('profile/',views.ManageUserView.as_view(),name='profile'),
    path('<int:user_id>/followers/',views.FollowerListView.as_view(),name='followers-list'),
    path('<int:user_id>/create_follow/',views.FollowCreateView.as_view(),name='follow'),
    path('<int:user_id>/unfollow/', views.UnfollowView.as_view(), name='user-unfollow'),
    path('followers/<int:user_id>/count/', views.FollowersCountView.as_view(), name='followers-count'),
]
