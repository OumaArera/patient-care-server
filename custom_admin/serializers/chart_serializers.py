from core.utils.non_empty_validator import NonEmptyListValidator
from custom_admin.models.chart import Chart
from custom_admin.models.patient import Patient
from rest_framework import serializers # type: ignore
from users.models import User  # type: ignore
from django.utils.timezone import localtime # type: ignore
from django.db.models import Q # type: ignore

class ChartSerializer(serializers.ModelSerializer):
    """Serializer for creating Chart entries."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()])
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    dateTaken = serializers.DateTimeField()

    class Meta:
        model = Chart
        fields = ["patient", "behaviors", "behaviorsDescription", "dateTaken"]

    def validate(self, data):
        patient = data.get("patient")
        date_taken = localtime(data.get("dateTaken")).date() 

        if Chart.objects.filter(
            Q(patient=patient) & 
            Q(dateTaken__date=date_taken)
        ).exists():
            raise serializers.ValidationError(
                "A chart entry for this patient already exists on this date."
            )

        return data



class ChartUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Chart entries, all fields are optional."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    careGiver1 = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    careGiver2 = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    behaviors = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    behaviorsDescription = serializers.JSONField(validators=[NonEmptyListValidator()], required=False)
    dateTaken = serializers.DateTimeField(required=False)

    class Meta:
        model = Chart
        fields = ["patient", "careGiver1", "careGiver2", "behaviors", "behaviorsDescription", "dateTaken"]



