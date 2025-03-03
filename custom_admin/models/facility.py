from django.db import models  # type: ignore
from django.core.exceptions import ValidationError # type: ignore

class Facility(models.Model):
    """Create facilities"""
    facilityId = models.AutoField(primary_key=True)
    facilityName = models.CharField(max_length=255, unique=False)
    facilityAddress = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Ensure facilityName is unique, case insensitive, only during creation."""
        if Facility.objects.exclude(pk=self.pk).filter(facilityName__iexact=self.facilityName).exists():
            raise ValidationError(f"A facility with name '{self.facilityName}' already exists.")
        
        super().save(*args, **kwargs)


    @classmethod
    def create_facility(cls, validated_data):
        """
        Create a new facilities instance from validated data.
        """
        facility = cls(**validated_data)
        return facility
