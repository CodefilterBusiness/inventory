from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Unit(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

