from django import forms

from hrms_api.models import *


class AptitudeTestForm(forms.ModelForm):
    class Meta:
        model = AptitudeTest
        fields = ['question', 'user_answer']
