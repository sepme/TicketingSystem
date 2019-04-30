from django.shortcuts import render, reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator

from .forms import CreateTicketForm, CreateMessageForm, UserSettingForm
from .models import Ticket, Message


@method_decorator(login_required(), name='dispatch')
class AddTicketView(TemplateView):
    template_name = 'ticket/add_ticket.html'
    extra_context = {'form': CreateTicketForm}

    def post(self, request):
        form = CreateTicketForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            priority = form.cleaned_data['priority']
            text = form.cleaned_data['message']
            attachment = form.cleaned_data['attachment']
            ticket = Ticket.objects.create(
                title=title,
                costumer=User.objects.get(id=request.user.id),
                priority=priority,
            )
            Message.objects.create(
                text=text,
                attachment=attachment,
                is_sent_by_costumer=True,
                ticket=ticket
            )
            return render(request, 'ticket/add_ticket.html', context={
                'form': form,
                'success_message': ticket.id
            })
        else:
            return render(request, 'ticket/add_ticket.html', context={
                'form': form,
                'fail_message': '2'
            })


@method_decorator(login_required(), name='dispatch')
class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket/list_ticket.html'
    context_object_name = 'ticket_list'

    def get_queryset(self):
        costumer = User.objects.get(id=self.request.user.id)
        return Ticket.objects.filter(costumer=costumer)


@method_decorator(login_required(), name='dispatch')
class UserSettingsView(TemplateView):
    template_name = 'ticket/user_setting.html'
    extra_context = {'form': UserSettingForm}

    def post(self, request):
        user = request.user
        form = UserSettingForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user-setting'))
        else:
            form = UserSettingForm(instance=user)
        context = {
            'form': form,
        }
        return render(request, 'ticket/user_setting.html', context)


@method_decorator(login_required(), name='dispatch')
class TicketDetailView(View):

    def get(self, request, *args, **kwargs):
        ticket_id = self.kwargs['ticket_id']
        ticket_detail = Ticket.objects.get(id=ticket_id)
        if ticket_detail.costumer.id == request.user.id:
            context = {
                'ticket': ticket_detail,
                'messages': Message.objects.filter(ticket=ticket_detail),
                'is_allowed': True,
                'form': CreateMessageForm
            }
            return render(request, 'ticket/ticket_detail.html', context=context)
        else:
            context = {'is_allowed': False}
            return render(request, 'ticket/ticket_detail.html', context=context)

    def post(self, request, *args, **kwargs):
        form = CreateMessageForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['message']
            attachment = form.cleaned_data['attachment']
            ticket_id = self.kwargs['ticket_id']
            Message.objects.create(
                text=text,
                attachment=attachment,
                is_sent_by_costumer=True,
                ticket=Ticket.objects.get(id=ticket_id)
            )
            context = {
                'ticket': Ticket.objects.get(id=ticket_id),
                'messages': Message.objects.filter(ticket=Ticket.objects.get(id=ticket_id)),
                'is_allowed': True,
                'form': CreateMessageForm
            }
            return render(request, 'ticket/ticket_detail.html', context=context)
