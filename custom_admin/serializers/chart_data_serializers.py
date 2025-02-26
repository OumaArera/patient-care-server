from core.utils.non_empty_validator import NonEmptyListValidator
from custom_admin.models.chart_data import ChartData
from rest_framework import serializers # type: ignore


class ChartDataSerializer(serializers.ModelSerializer):
    """Deserializer for creating ChartData."""

    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=True)

    class Meta:
        model = ChartData
        fields = ["behaviors", "vitals", "behaviorsDescription"]


class ChartDataUpdateSerializer(serializers.ModelSerializer):
    """Deserializer for updating ChartData, all fields are optional."""

    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    vitals = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)

    class Meta:
        model = ChartData
        fields = ["behaviors", "vitals", "behaviorsDescription"]