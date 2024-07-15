from django.db import models
from stocks.models import Stock
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class Outbound(models.Model):
    transaction_ref = models.CharField(max_length=100, unique=True, editable=False)  # Unique transaction reference
    items = models.ManyToManyField(Stock, through='OutboundItem')  # Many-to-many relation with Stock through OutboundItem
    outbound_date = models.DateTimeField(default=timezone.now)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.transaction_ref:
            self.transaction_ref = self.generate_transaction_ref()

        super().save(*args, **kwargs)

    def generate_transaction_ref(self):
        return uuid.uuid4().hex[:10].upper()  # Generate a unique transaction reference

    def __str__(self):
        return self.transaction_ref

def generate_transaction_ref():
    # Generate a unique transaction reference
    # You can implement your own logic to generate the reference here
    # For example, combining a prefix with a timestamp or using a UUID
    return 'TR-' + timezone.now().strftime('%Y%m%d%H%M%S%f')



class OutboundItem(models.Model):
    outbound = models.ForeignKey(Outbound, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Deduct the quantity from the Stock item
        self.stock.quantity -= self.quantity
        if self.stock.quantity < 0:
            raise ValueError('Stock quantity cannot be negative.')
        self.stock.save()

    def delete(self, *args, **kwargs):
        # When an OutboundItem is deleted, return the quantity to the Stock item
        self.stock.quantity += self.quantity
        self.stock.save()
        super().delete(*args, **kwargs)

