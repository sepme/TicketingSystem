from django.urls import path
from ticket.views import AddTicketView, TicketListView, TicketDetailView, UserSettingsView

urlpatterns = [
    path('', TicketListView.as_view(), name='profile'),
    path('add/', AddTicketView.as_view(), name='add-ticket'),
    path('detail/<int:ticket_id>', TicketDetailView.as_view(), name='ticket-detail'),
    path('change/', UserSettingsView.as_view(), name='user-setting'),
]
