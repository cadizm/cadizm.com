
from django.contrib.gis.db import models

class Bookmark(models.Model):
    name = models.CharField(max_length=128)
    url_yelp = models.CharField(max_length=1024)
    addr = models.CharField(max_length=128)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=32)
    zip = models.CharField(max_length=16)
    phone = models.CharField(max_length=32)
    geom = models.PointField(srid=4326)
    # override the default manager with a GeoManager instance.
    objects = models.GeoManager()

    # Returns the string representation of the model.
    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.name
