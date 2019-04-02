from django import forms

class ChangeForm(forms.Form):
	name = forms.CharField()
	
class AddForm(forms.Form):
	MN = forms.IntegerField()
	