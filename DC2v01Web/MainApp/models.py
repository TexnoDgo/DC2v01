from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from WorkApp.models import Project, Order


# Create your models here.
class Profile(models.Model):
    ROOT_STATUS_LIST = (
        ('DESIGNER', 'DESIGNER'),
        ('PRODUCTION', 'PRODUCTION'),
        ('GUEST', 'GUEST')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    root_status = models.CharField(max_length=100, choices=ROOT_STATUS_LIST, default='GUEST')
    active_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    active_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, default='+38(099) 099-99-99')
    new_email = models.CharField(max_length=100, default='new_net@gmail.com')
    profile_user_name = models.CharField(max_length=20, default='Имя')
    profile_user_last = models.CharField(max_length=20, default='Фамилия')

    def __str__(self):
        return "Profile: " + self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()