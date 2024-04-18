from django import forms

from hrms_api.models import *


class GroupChatForm(forms.ModelForm):

    class Meta:
        model = GroupConversation
        fields = ['name', 'group_avatar']


class AddGroupMemberForm(forms.ModelForm):
    member = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = GroupMember
        fields = ['member']
        widgets = {
            'member': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
