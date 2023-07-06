from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy, reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, verbose_name="Аватар")
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="URL")
    address = models.CharField(max_length=250, verbose_name='Адрес', blank=True, default='Адрес не указан')
    phone = PhoneNumberField(null=False, blank=True, verbose_name='Номер телефона', default='Номер не указан')
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, default='Город не установлен')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:profile_detail', kwargs={'slug': self.slug})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
