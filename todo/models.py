from django.db import models
from django.contrib.auth.models import User

class Invite(models.Model):
    host_name = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.host_name