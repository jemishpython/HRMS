from django import forms

from hrms_api.models import *


class GroupChatForm(forms.ModelForm):

    class Meta:
        model = GroupConversation
        fields = ['name', 'group_avatar', 'receiver']
        widgets = {
            'receiver': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

        receiver = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )