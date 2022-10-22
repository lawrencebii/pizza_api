from django.urls import path

from . import views

urlpatterns = [
    # path('', views.HelloAuthView.as_view(), name='hello_auth'),
    path('signup/', views.UserCreateView.as_view(), name='signUp '),
    path('users/', views.AllUsersView.as_view(), name='all-users')
    # path('users/<int:pk>',views.AllUsersView.as_view())
]
