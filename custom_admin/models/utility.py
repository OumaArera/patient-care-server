from django.db import models
from users.models import User


class Utility(models.Model):
    """Utilities management"""

    utilityId = models.AutoField(primary_key=True)
    staff =  models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='utilities'
    )
    item = models.CharField(max_length=255)
    details = models.TextField()
    STATUS_CHOICES = [
        ('addressed', 'Addressed'),
        ('review', 'Review'),
        ('pending', 'Pending')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_utility(cls, validated_data):
        """
        Create a new utility instance from validated data.
        """
        new_utility = cls(**validated_data)
        return new_utility