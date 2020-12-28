from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.
class Bus(models.Model):
	name = models.CharField(max_length=200)
	from_location = models.CharField(max_length=200)
	to_location = models.CharField(max_length=200)
	total_seats = models.PositiveIntegerField()
	available_seats = models.PositiveIntegerField()
	price = models.PositiveIntegerField(validators=[MinValueValidator(1)])

	
	def __str__(self):
		return self.name

