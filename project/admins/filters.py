import django_filters
from .models import Bus

class BusFilter(django_filters.FilterSet):
	class Meta:
		model = Bus
		fields = '__all__'
		exclude = ['total_seats', 'available_seats','price']