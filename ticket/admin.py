from django.contrib import admin
from .models import Ticket, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 1
    fields = ['text', 'attachment']



@admin.register(Ticket)
class ResponderAdmin(admin.ModelAdmin):
    fields = ['title', 'costumer', 'priority']
    inlines = [MessageInline]
