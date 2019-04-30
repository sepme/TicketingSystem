from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/', include('ticket.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
