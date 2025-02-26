from django.db import models # type: ignore

class ChartData(models.Model):
    """Create charts data"""
    chartDataId = models.AutoField(primary_key=True)
    behaviors = models.JSONField()
    behaviorsDescription = models.JSONField()
    vitals = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)
    

    @classmethod
    def create_chart_data(cls, validated_data):
        """
        Create a new charts data instance from validated data.
        """
        new_chart_data = cls(**validated_data)
        return new_chart_data

