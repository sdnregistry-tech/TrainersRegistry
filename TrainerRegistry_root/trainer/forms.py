from django import forms
from .models import Trainer  # Ensure you have a Trainer model
from .models import Qualification
from django.contrib.auth.forms import SetPasswordForm


# forms.py
class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'birthdate', 'address', 'email', 'contact_number']

class QualificationForm(forms.ModelForm):
    validity_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Qualification
        fields = ['certificate_name', 'nttc_number', 'validity_date']



# forms.py
from django import forms

class QualificationReportForm(forms.Form):
    name = forms.CharField(required=False, label='Trainer Name')
    certificate_name = forms.CharField(required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password1'})
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password2'})
    )




