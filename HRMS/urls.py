from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from admin_app import views
from employee_app.views import landing

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", landing, name='landing'),
    path("hrms-admin/", include('admin_app.urls')),
    path("hrms/employee/", include('employee_app.urls')),
    path("hrms/", include('hrms_api.urls')),
    path('hrms/login_admin/', views.Login, name="Login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
