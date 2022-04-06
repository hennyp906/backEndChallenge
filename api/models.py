import uuid
from django.db import models

from django.contrib.auth import get_user_model

from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)

# Create your models here.

User = get_user_model()

alphanumeric = RegexValidator(
    r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
)


class Bond(models.Model):
    STATUS = (
        ("purchased", "PURCHASED"),
        ("available", "AVAILABLE"),
    )
    name = models.CharField(
        max_length=40, validators=[alphanumeric, MinLengthValidator(3)]
    )
    numberOfBonds = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)]
    )
    price = models.DecimalField(max_digits=13, decimal_places=4)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    publishedBy = models.ForeignKey(
        User, related_name="publisher", on_delete=models.CASCADE
    )
    isPurchased = models.CharField(max_length=50, choices=STATUS, default="available")
    purchasedBy = models.ForeignKey(
        User, related_name="buyer", on_delete=models.SET_NULL, null=True, blank=True
    )
    priceInUSD = models.DecimalField(
        max_digits=13, decimal_places=4, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Bond, self).save(*args, **kwargs)
