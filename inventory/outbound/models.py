from django.db import models
from stocks.models import Stock
from profiles.models import Unit
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Outbound(models.Model):
    transaction_ref = models.CharField(max_length=100, unique=True, editable=False)
    customer = models.CharField(max_length=50, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    items = models.ManyToManyField(Stock, through='OutboundItem')
    outbound_date = models.DateTimeField(default=timezone.now)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.transaction_ref:
            self.transaction_ref = self.generate_transaction_ref()
        super().save(*args, **kwargs)

    def generate_transaction_ref(self):
        return uuid.uuid4().hex[:10].upper()

    def __str__(self):
        return self.transaction_ref


class OutboundItem(models.Model):
    outbound = models.ForeignKey('Outbound', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the outbound quantity exceeds available stock
        if self.quantity > self.stock.quantity:
            raise ValueError(f"Stock quantity for '{self.stock.stock_no}' cannot be negative or zero.")

        # Deduct the outbound quantity from stock
        self.stock.quantity -= self.quantity
        self.stock.save()

    def delete(self, *args, **kwargs):
        # Return quantity to stock when deleting an outbound item
        self.stock.quantity += self.quantity
        self.stock.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.stock} - {self.quantity}'