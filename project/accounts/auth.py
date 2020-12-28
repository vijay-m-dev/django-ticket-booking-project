from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
	def authenticate(self, request, username=None, email=None, password=None, **kwargs):
		UserModel=get_user_model()
		if username:
			try:
				user=UserModel.objects.get(username=username)
			except UserModel.DoesNotExist:
				return None
			else:
				if user.check_password(password):
					return user
		else:
			try:
				user=UserModel.objects.get(email=email)
			except UserModel.DoesNotExist:
				return None
			else:
				if user.check_password(password):
					return user

