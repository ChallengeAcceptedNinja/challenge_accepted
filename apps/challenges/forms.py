from django import forms

class ChallengeInitiateForm(forms.Form):
    challenge_name = forms.CharField(label="Challenge Name", max_length=100)
    description = forms.CharField(label="Description", max_length=100)
    start_date = forms.DateField(label="Commencement Date")
    signup_end_date = forms.DateField(label="Sign-up End Date")