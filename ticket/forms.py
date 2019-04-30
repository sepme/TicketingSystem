from django import forms
from django.contrib.auth.models import User
from .models import Ticket, PRIORITIES


class UserSettingForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'نام کاربری',
            'email': 'پست الکترونیک',
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
        }


class CreateTicketForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, label="عنوان:")
    priority = forms.ChoiceField(choices=PRIORITIES, required=True, label="اولویت:")
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, label="پیام:")
    attachment = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), label="ضمیمه:", required=False)

    def __init__(self, *args, **kwargs):
        super(CreateTicketForm, self).__init__(*args, **kwargs)
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})


class CreateMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}), required=True, label="پیام:")
    attachment = forms.FileField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), label="ضمیمه:", required=False)
