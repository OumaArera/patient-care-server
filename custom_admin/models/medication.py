from django.db import models # type: ignore

from custom_admin.models.patient import Patient  # type: ignore

class Medication(models.Model):
    """Create medications"""
    medicationId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
		Patient,
		on_delete=models.CASCADE,
		related_name='medications'
	)
    medicationName = models.CharField(max_length=255)
    medicationCode = models.CharField(max_length=50)
    equivalentTo = models.CharField(max_length=255)
    instructions = models.TextField()
    quantity = models.CharField(max_length=255)
    diagnosis = models.TextField()
    medicationTime = models.DateTimeField()
    STATUS_CHOICES = [
        ('active', 'Active Medication'),
        ('stale', 'Stale Medication'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_medication(cls, validated_data):
        """
        Create a new medications instance from validated data.
        """
        new_medication = cls(**validated_data)
        return new_medication

