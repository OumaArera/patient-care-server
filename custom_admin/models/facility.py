from django.db import models  # type: ignore

class Facility(models.Model):
    """Create facilities"""
    facilityId = models.AutoField(primary_key=True)
    facilityName = models.CharField(max_length=255)
    facilityAddress = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_facility(cls, validated_data):
        """
        Create a new facilities instance from validated data.
        """
        facility = cls(**validated_data)
        return facility

