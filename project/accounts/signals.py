from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from passengers.models import Passenger

@receiver(post_save,sender=get_user_model())
def passenger_profile(sender, instance, created, **kwargs):
	if created:
		try:
			group = Group.objects.get(name='admins')
		except:
			group=Group()
			group.name='admins'
			group.save()
		try:
			group = Group.objects.get(name='passengers')
		except:
			group=Group()
			group.name='passengers'
			group.save()
		if instance.is_superuser:
			group = Group.objects.get(name='admins')
		else:
			group = Group.objects.get(name='passengers')
			Passenger.objects.create(user=instance,name=instance.username)
		instance.groups.add(group)
		

