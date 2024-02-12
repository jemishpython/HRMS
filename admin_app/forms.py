from django import forms

from hrms_api.models import Holiday

class EditHolidaysForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# class EditHolidaysForm(forms.ModelForm):
#     class Meta:
#             model = Holiday
#             fields = ['holiday_title,', 'holiday_date']