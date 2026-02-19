from django.db import models
from django.conf import settings


class Favourite(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=50)
    status = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    phrases = models.TextField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    image = models.URLField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'name', 'occupation'),)

    def __str__(self):
        return self.name + ' - Status: ' + (self.status if self.status else 'Unknown')
