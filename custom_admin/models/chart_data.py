from django.db import models # type: ignore
from custom_admin.models.patient import Patient

class ChartData(models.Model):
    """Create charts data"""
    chartDataId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
		Patient,
		on_delete=models.CASCADE,
		related_name='charts_data'
	)
    behaviors = models.JSONField()
    behaviorsDescription = models.JSONField()
    timeToBeTaken = models.TimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    

    @classmethod
    def create_chart_data(cls, validated_data):
        """
        Create a new charts data instance from validated data.
        """
        new_chart_data = cls(**validated_data)
        return new_chart_data

