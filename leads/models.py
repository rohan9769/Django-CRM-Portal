from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Lead(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    phoned = models.BooleanField(default=False)
    agent = models.ForeignKey("Agent",on_delete=models.CASCADE) #CASCADE means if agnent is deleted then the Lead will also get deleted
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name


