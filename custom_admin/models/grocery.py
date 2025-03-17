from django.db import models
from users.models import User


class Grocery(models.Model):
    """Handles groceries"""

    groceryId = models.AutoField(primary_key=True)
    staff =  models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='groceries'
    )
    details = models.JSONField(default=list)
    feedback = models.TextField(null=True, blank=True, default=None)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('updated', 'Updated')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_grocery(cls, validated_data):
        """
        Create a new grocery instance from validated data.
        """
        new_grocery = cls(**validated_data)
        return new_grocery