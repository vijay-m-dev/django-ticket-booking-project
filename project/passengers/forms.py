from django.forms import ModelForm
from .models import Passenger

class ProfileForm(ModelForm):
	class Meta:
		model = Passenger
		fields = ['name', 'email', 'phone']