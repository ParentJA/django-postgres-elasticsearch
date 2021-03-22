import uuid

from django.db import models


class Wine(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    country = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    points = models.IntegerField()
    price = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True
    )
    variety = models.CharField(max_length=255)
    winery = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.id}'
