from rest_framework import serializers
from custom_admin.models.leave import Leave

class LeaveSerializer(serializers.ModelSerializer):
    """Serializer for creating a Leave instance."""
    
    reasonForLeave = serializers.CharField(required=True)
    startDate = serializers.DateField()
    endDate = serializers.DateField()
    status = serializers.ChoiceField(choices=['approved', 'declined', 'pending'], default='pending', read_only=True)
    declineReason = serializers.CharField(required=False, allow_null=True, allow_blank=True, read_only=True)
    
    class Meta:
        model = Leave
        fields = [
            "leaveId", "staff", "reasonForLeave", "startDate", "endDate", "status", "declineReason",
            "createdAt", "modifiedAt"
        ]
        read_only_fields = ["leaveId", "createdAt", "modifiedAt", "status", "declineReason", "staff"]

    def validate(self, data):
        """Validate that start date is before end date."""
        start_date = data.get("startDate")
        end_date = data.get("endDate")
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                "endDate": "End date must be after start date."
            })
        
        return data


class LeaveUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Leave instance."""
    
    reasonForLeave = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    startDate = serializers.DateField(required=False)
    endDate = serializers.DateField(required=False)
    status = serializers.ChoiceField(required=False, choices=['approved', 'declined', 'pending'])
    declineReason = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = Leave
        fields = [
            "reasonForLeave", "startDate", "endDate", "status", "declineReason"
        ]
    
    def validate(self, data):
        """Ensure the leave update maintains valid date constraints."""
        start_date = data.get("startDate", self.instance.startDate if self.instance else None)
        end_date = data.get("endDate", self.instance.endDate if self.instance else None)
        
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({
                "endDate": "End date must be after start date."
            })
        
        return data
