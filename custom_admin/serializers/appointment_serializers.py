from custom_admin.models.appointment import Appointment
from custom_admin.models.patient import Patient
from rest_framework import serializers

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for creating appointments entries."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=True)
    details = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=[
        'Primary Care Provider (PCP)',
        'Mental Health Provider / Physician/ Prescriber',
        'Clinician', "Dentist", "Peer Support Counsellor",
        "Counsellor", "Specialist", "Other"
    ], required=True)
    nextAppointmentDate = serializers.DateField(required=True)
    dateTaken = serializers.DateField(required=True)

    class Meta:
        model = Appointment
        fields = ["patient", "details", "type", "nextAppointmentDate", "dateTaken"]



class AppointmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating Appointment entries, all fields are optional."""
    details = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=[
        'Primary Care Provider (PCP)',
        'Mental Health Provider / Physician/ Prescriber',
        'Clinician', "Dentist", "Peer Support Counsellor",
        "Counsellor", "Specialist", "Other"
    ], required=False)
    nextAppointmentDate = serializers.DateField(required=False)
    dateTaken = serializers.DateField(required=False)

    class Meta:
        model = Appointment
        fields = ["details", "type", "nextAppointmentDate", "dateTaken"]

