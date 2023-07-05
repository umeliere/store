from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True, default='Не выбрано')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True, default='Не выбрано')
    address = models.CharField(max_length=250, verbose_name='Адрес', blank=True, default='Не выбрано')
    phone = PhoneNumberField(null=False, blank=True, verbose_name='Номер телефона', default='Не выбрано')
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, default='Не выбрано')

    def get_absolute_url(self):
        return reverse_lazy('users:profile_detail', kwargs={'pk': self.pk})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
