from django import forms

class MedicationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label='Medication or Message')