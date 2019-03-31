from django import forms

class ChangeForm(forms.Form):
	MN = forms.CharField()
	
class AddForm(forms.Form):
	MN = forms.IntegerField()
	