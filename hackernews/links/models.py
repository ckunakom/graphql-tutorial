from django.db import models
from django.conf import settings

# Every time there's a change in the below class,
# make sure to run the following in cmd:
# python manage.py makemigrations
# python manage.py migrate

# Create your models here.
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    # Create your own links posted by you
    # Since sign-in power is acquired
    # Integrate links and users models
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

