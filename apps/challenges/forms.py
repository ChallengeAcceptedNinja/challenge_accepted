from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import TextInput, DateInput
import datetime
from functools import partial



class ChallengeInitiateForm(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})
    challenge_name = forms.CharField(label="Challenge Name", max_length=100)
    description = forms.CharField(widget=forms.Textarea, label="Description")
    signup_end_date = forms.DateField(widget=DateInput(), label="Sign-up End Date")
    start_date = forms.DateField(widget=DateInput(), label="Commencement Date")

    def clean_start_date(self):
        start_date=self.cleaned_data['start_date']
        if start_date < datetime.date.today():
            raise forms.ValidationError("The start date cannot be in the past.")
        else:
            return start_date

    def clean_signup_end_date(self):
        start_date = datetime.datetime.strptime(self.data['start_date'], '%m/%d/%Y')
        signup_end_date = datetime.datetime.strptime(self.data['signup_end_date'], '%m/%d/%Y')
        if signup_end_date >= start_date:
            raise forms.ValidationError("The sign-up end date cannot come after the commencement date.")
        else:
            return signup_end_date
