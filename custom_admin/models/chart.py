from django.db import models # type: ignore

from custom_admin.models.patient import Patient
from users.models import User  # type: ignore

class Chart(models.Model):
    """Create charts"""
    chartId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
		Patient,
		on_delete=models.CASCADE,
		related_name='charts'
	)
    careGiver1 =  models.ForeignKey(
		User,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='first_care_giver'
	)
    careGiver2 =  models.ForeignKey(
		User,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='second_care_giver'
	)
    behaviors = models.JSONField()
    behaviorsDescription = models.JSONField()
    dateTaken = models.DateField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_chart(cls, validated_data):
        """
        Create a new charts instance from validated data.
        """
        new_chart = cls(**validated_data)
        return new_chart

