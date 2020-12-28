from django import forms
from .models import Bus

class BusForm(forms.ModelForm):
	class Meta:
		model = Bus
		fields = '__all__'

	def clean_available_seats(self,*args,**kwargs):
		available_seats=self.cleaned_data.get('available_seats')
		total_seats=self.cleaned_data.get('total_seats')
		if available_seats > total_seats:
			raise forms.ValidationError("Available seats must not be greater than total seats")
		return available_seats