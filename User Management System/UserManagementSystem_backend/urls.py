from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.tokens import EmailTokenObtainPairView  # ✅ bizim özel token view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),#token alma
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),#refresh tokenı alma
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
