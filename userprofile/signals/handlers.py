from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from userprofile.models import UserProfile

@receiver(post_save, sender=User) # Connect to the signal post_save.
def handle_user_save(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)