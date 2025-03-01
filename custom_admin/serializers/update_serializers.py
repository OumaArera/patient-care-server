from datetime import timedelta
from django.utils.timezone import now
from rest_framework import serializers
from custom_admin.models.update import Update
from custom_admin.models.patient import Patient

class UpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating an Update instance."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    notes = serializers.CharField()
    dateTaken = serializers.DateField()
    type = serializers.ChoiceField(required=True, choices=['weekly', 'monthly'])
    weight = serializers.IntegerField(min_value=0, required=False)
    weightDeviation = serializers.IntegerField(required=False, read_only=True)  # Auto-calculated field

    class Meta:
        model = Update
        fields = [
            "updateId", "patient", "notes", "dateTaken", "weight", "type", "weightDeviation",
            "createdAt", "modifiedAt"
        ]
        read_only_fields = ["updateId", "createdAt", "modifiedAt", "weightDeviation"]

    def validate(self, data):
        """Perform validation to ensure monthly updates are unique per month, and weekly updates per week."""
        patient = data.get("patient")
        date_taken = data.get("dateTaken")
        update_type = data.get("type")
        weight = data.get("weight")

        if update_type == "weekly":
            # Ensure only one weekly update exists per week for the given patient
            start_of_week = date_taken - timedelta(days=date_taken.weekday())  # Monday of the same week
            end_of_week = start_of_week + timedelta(days=6)  # Sunday of the same week

            existing_weekly_update = Update.objects.filter(
                patient=patient, type="weekly",
                dateTaken__range=(start_of_week, end_of_week)
            ).exists()

            if existing_weekly_update:
                raise serializers.ValidationError({
                    "dateTaken": "A weekly update already exists for this resident in the selected week."
                })

            # Weekly updates: weight and weightDeviation should not be required
            data.pop("weight", None)
            data.pop("weightDeviation", None)

        elif update_type == "monthly":
            if weight is None:
                raise serializers.ValidationError({"weight": "Weight is required for monthly updates."})

            # Ensure only one monthly update exists per month for the given patient
            start_of_month = date_taken.replace(day=1)  # First day of the current month
            next_month = (date_taken.replace(day=28) + timedelta(days=4)).replace(day=1)  # First day of next month
            end_of_month = next_month - timedelta(days=1)  # Last day of the current month

            existing_monthly_update = Update.objects.filter(
                patient=patient, type="monthly",
                dateTaken__range=(start_of_month, end_of_month)
            ).exists()

            if existing_monthly_update:
                raise serializers.ValidationError({
                    "dateTaken": "A monthly update already exists for this resident in the selected month."
                })

            # Get the first and last day of the previous month
            first_day_of_prev_month = (start_of_month - timedelta(days=1)).replace(day=1)
            last_day_of_prev_month = start_of_month - timedelta(days=1)  # Last day of previous month

            # Retrieve the most recent monthly update from the previous month
            last_monthly_update = (
                Update.objects.filter(
                    patient=patient, 
                    type="monthly", 
                    dateTaken__range=(first_day_of_prev_month, last_day_of_prev_month)
                )
                .order_by("-dateTaken")
                .first()
            )

            if last_monthly_update and last_monthly_update.weight is not None:
                data["weightDeviation"] = weight - last_monthly_update.weight
            else:
                data["weightDeviation"] = 0  # No previous data, set deviation to 0

        return data


class UpdateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating an Update instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    notes = serializers.CharField(required=False)
    dateTaken = serializers.DateField(required=False)
    type = serializers.ChoiceField(required=False, choices=['weekly', 'monthly'])
    weight = serializers.IntegerField(min_value=0, required=False)

    class Meta:
        model = Update
        fields = [
            "patient", "notes", "dateTaken", "weight", "type"
        ]
