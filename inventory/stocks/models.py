from django.db import models
from django.contrib.auth.models import User  # Assuming you use Django's built-in User model
from django.utils import timezone

class Stock(models.Model):
    stock_no = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.IntegerField()
    available = models.BooleanField(default=True)
    remarks = models.TextField(blank=True, null=True)
    last_modified_date = models.DateTimeField(default=timezone.now)
    entry_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if the instance is being updated
        if self.pk:
            # Set the modified_by field to the currently logged-in user
            self.modified_by = kwargs.pop('modified_by', None)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.stock_no  # Display stock number as the object's string representation
