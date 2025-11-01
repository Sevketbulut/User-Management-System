
from django.http import HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
import csv
import re

from .models import User, UserLog
from .serializers import UserSerializer, UserLogSerializer
from .permissions import RoleBasedPermission

#kullanıcı CRUD ve loglarını yöneten APIlar
class UserViewSet(viewsets.ModelViewSet):

    #Kullanıcı CRUD işlemleri + otomatik log kaydı
    #Admin -> Full Access
    #Manager -> Read + Update
    #User -> Read Only

    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [RoleBasedPermission]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'department', 'status']
    search_fields = ['name', 'email', 'department', 'role', 'status']
    ordering_fields = ['created_at', 'name', 'email']
    ordering = ['-created_at']

    def validate_email(self, email):
        #gmail ve hotmail domaini izinli
        allowed_domains = ['gmail.com', 'hotmail.com']
        domain = email.split('@')[-1].lower()
        if domain not in allowed_domains:
            raise ValidationError("Only gmail.com or hotmail.com addresses are allowed.")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValidationError("Invalid email format.")
        return email

    def perform_create(self, serializer):
        data = serializer.validated_data
        required_fields = ['name', 'email', 'role', 'department', 'status']
        for field in required_fields:
            if not data.get(field):
                raise ValidationError(f"{field.capitalize()} field is required.")

        self.validate_email(data['email'])
        instance = serializer.save()

        UserLog.objects.create(
            user=instance,
            action='create',
            performed_by=self.request.user.email if self.request.user.is_authenticated else 'admin@test.com',
            changes={'info': f'User {instance.name} created'}
        )

    def perform_update(self, serializer):
        data = serializer.validated_data
        if 'email' in data:
            self.validate_email(data['email'])

        instance = serializer.save()
        UserLog.objects.create(
            user=instance,
            action='update',
            performed_by=self.request.user.email if self.request.user.is_authenticated else 'admin@test.com',
            changes={'info': f'User {instance.name} updated'}
        )

    def perform_destroy(self, instance):
        user_name = instance.name
        user_email = instance.email
        UserLog.objects.create(
            user=instance,
            action='delete',
            performed_by=self.request.user.email if self.request.user.is_authenticated else 'admin@test.com',
            changes={'info': f'User {user_name} ({user_email}) deleted'}
        )
        instance.delete()

#Kullanıcı listesini export eder(Sadece admin)
@api_view(['GET'])
def export_users_csv(request):

    if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'admin':
        return Response({"detail": "Only admin users can export data."}, status=status.HTTP_403_FORBIDDEN)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Role', 'Department', 'Status', 'Phone', 'Created', 'Updated'])

    users = User.objects.all()
    for u in users:
        writer.writerow([u.name, u.email, u.role, u.department, u.status, u.phone, u.created_at, u.updated_at])

    return response

#Kullanıcı hareketlerini listeleyen endpoint
class UserLogViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = UserLog.objects.all().order_by('-timestamp')
    serializer_class = UserLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'performed_by']
    search_fields = ['user_name', 'user_email']
