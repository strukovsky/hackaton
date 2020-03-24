from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', max_length=100)

class AlgorithmForm(forms.Form):
    name = forms.CharField(label='Name of algorithm', max_length=50)
    code = forms.CharField(label='Code of algo', max_length=4096, widget=forms.Textarea)
