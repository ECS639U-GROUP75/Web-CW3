from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    Hobbies = models.ManyToManyField('Hobby', related_name='users')
    
    groups = models.ManyToManyField('auth.Group', related_name='customeruser_set', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customeruser_set', blank=True,)

    def __str__(self):
        return self.username
    
class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# idk what this is for, it was here before so I'm leaving it here
# class PageView(models.Model):
#     count = models.IntegerField(default=0)

#     def __str__(self):
#         return f"Page view count: {self.count}"
