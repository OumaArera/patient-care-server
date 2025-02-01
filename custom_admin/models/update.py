from django.db import models # type: ignore

from custom_admin.models.patient import Patient
from users.models import User  # type: ignore

class Update(models.Model):
    """Create updates"""
    updateId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
		Patient,
		on_delete=models.CASCADE,
		related_name='updates'
	)
    careGiver =  models.ForeignKey(
		User,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='updates'
	)
    notes = models.TextField()
    dateTaken = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_update(cls, validated_data):
        """
        Create a new charts instance from validated data.
        """
        new_update = cls(**validated_data)
        return new_update

