from django.db import models
from django.contrib.auth import get_user_model
from admins.models import Bus
from django.conf import settings
from django.core.validators import MinValueValidator


class Passenger(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	
	def __str__(self):
		return self.name

class Booking(models.Model):
	passenger = models.ForeignKey(Passenger, on_delete= models.CASCADE)
	bus = models.ForeignKey(Bus, on_delete= models.CASCADE)
	no_of_tickets = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	total_cost = models.PositiveIntegerField(validators=[MinValueValidator(1)])

	def compute_total_cost(self):
		total_cost=self.no_of_tickets*self.bus.price
		return total_cost

	def save(self, *args, **kwargs):
		self.total_cost=self.compute_total_cost()
		super(Booking, self).save(*args, **kwargs)

	def __str__(self):
		return 'booking'+str(self.id)