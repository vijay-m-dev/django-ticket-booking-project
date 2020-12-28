from django.db.models.signals import pre_delete
from django.dispatch import receiver
from passengers.models import Booking


@receiver(pre_delete,sender=Booking, dispatch_uid='bus_delete_signal')
def bus_tickets_update(sender, instance, using, **kwargs):
	bus=instance.bus
	bus.available_seats+=instance.no_of_tickets
	bus.save()