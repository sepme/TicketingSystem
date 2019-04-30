from django.db import models
from django.contrib.auth.models import User
from TicketingSystem.settings import BASE_DIR
import os


PRIORITIES = {
    ("0", "معمولی"),
    ("1", "نیمه فوری"),
    ("2", "فوری")
}

SITUATIONS = {
        ("NS", "Solved"),
        ("SO", "Not Solved")
    }


def user_url_pattern(instance, filename):
    return '/u_{0}/{1}'.format(instance.ticket.costumer.id, filename)


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    date_submitted = models.DateTimeField(auto_now_add=True)
    costumer = models.ForeignKey(User, on_delete=models.PROTECT)
    situation = models.CharField(max_length=2, editable=False, choices=SITUATIONS)
    priority = models.CharField(max_length=2, choices=PRIORITIES, default="0")

    def get_url(self):
        url = 'detail/%s' % self.id
        return url

    def __str__(self):
        return self.title

    def is_answered(self):
        status = Message.objects.filter(ticket=self).order_by('-id')[0].is_sent_by_costumer
        return not status


class Message(models.Model):
    text = models.TextField()
    attachment = models.FileField(upload_to='', blank=True)
    is_sent_by_costumer = models.BooleanField(default=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    date_sent = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '#%s' % str(self.id)
