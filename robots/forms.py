from django import forms


class JSONForm(forms.Form):
    json = forms.JSONField()