from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router_users = DefaultRouter()
router_users.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path(
        'auth/signup/',
        views.SignUpView.as_view(),
        name='signup'
    ),
    path(
        'auth/token/',
        views.JWTTokenView.as_view(),
        name='jwt_token'
    ),
    path('', include(router_users.urls)),
]
