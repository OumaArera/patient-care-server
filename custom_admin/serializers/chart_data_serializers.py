from core.utils.non_empty_validator import NonEmptyListValidator
from custom_admin.models.chart_data import ChartData
from custom_admin.models.patient import Patient
from rest_framework import serializers # type: ignore


class ChartDataSerializer(serializers.ModelSerializer):
    """Deserializer for creating ChartData."""

    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    timeToBeTaken = serializers.TimeField()

    class Meta:
        model = ChartData
        fields = ["patient", "behaviors", "vitals", "behaviorsDescription", "timeToBeTaken"]


class ChartDataUpdateSerializer(serializers.ModelSerializer):
    """Deserializer for updating ChartData, all fields are optional."""

    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    timeToBeTaken = serializers.TimeField(required=False)
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)

    class Meta:
        model = ChartData
        fields = ["patient", "behaviors", "vitals", "behaviorsDescription", "timeToBeTaken"]