from django.contrib import admin
from django.urls import path, include
from ticket.views import UserCreationView, Index

urlpatterns = [
    path('', Index),
    path('admin/', admin.site.urls),
    path('profile/', include('ticket.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/sign-up', UserCreationView.as_view(), name='sign-up'),
]
