from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserLogViewSet, export_users_csv

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-logs', UserLogViewSet, basename='userlog')

urlpatterns = [
    path('', include(router.urls)),
    path('export-users/', export_users_csv, name='export_users'),
]
