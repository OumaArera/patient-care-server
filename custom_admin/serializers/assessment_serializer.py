from rest_framework import serializers
from custom_admin.models.patient import Patient
from custom_admin.models.assessment import Assessment


class AssessmentSerializer(serializers.ModelSerializer):
    """Serializer for creating an Assessment instance."""
    resident = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)

    class Meta:
        model = Assessment
        fields = [
            "assessmentId", "resident", "assessmentStartDate", "assessmentNextDate",
            "NCPStartDate", "NCPNextDate", "socialWorker", "createdAt", "modifiedAt"
        ]
        read_only_fields = ["assessmentId", "createdAt", "modifiedAt"]

    def validate(self, data):
        """Additional validation if needed."""
        return data


class AssessmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating an Assessment instance."""
    resident = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False, allow_null=True)
    assessmentStartDate = serializers.DateField(required=False, allow_null=True)
    assessmentNextDate = serializers.DateField(required=False, allow_null=True)
    NCPStartDate = serializers.DateField(required=False, allow_null=True)
    NCPNextDate = serializers.DateField(required=False, allow_null=True)
    socialWorker = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Assessment
        fields = ["resident", "assessmentStartDate", "assessmentNextDate", "NCPStartDate", "NCPNextDate", "socialWorker"]
