from rest_framework import serializers
from custom_admin.models.late_submission import LateSubmission
from custom_admin.models.patient import Patient
from users.models import User

class LateSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for creating a LateSubmission instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    careGiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    type = serializers.ChoiceField(required=True, choices=['charts', 'medication', 'updates', 'vital'])
    start = serializers.DateTimeField(required=True)
    duration = serializers.IntegerField(required=True)
    reasonForLateSubmission = serializers.CharField(required=True)
    
    class Meta:
        model = LateSubmission
        fields = [
            "lateSubmissionId", "patient", "careGiver", "type", "start", "duration", 
            "reasonForLateSubmission", "createdAt", "modifiedAt"
        ]
        read_only_fields = ["lateSubmissionId", "createdAt", "modifiedAt"]


class LateSubmissionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a LateSubmission instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    manager = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    careGiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    type = serializers.ChoiceField(required=False, choices=['charts', 'medication', 'updates', 'vital'])
    start = serializers.DateTimeField(required=False)
    duration = serializers.IntegerField(required=False)
    reasonForLateSubmission = serializers.CharField(required=False)
    
    class Meta:
        model = LateSubmission
        fields = ["patient", "manager", "careGiver", "type", "start", "duration", "reasonForLateSubmission"]